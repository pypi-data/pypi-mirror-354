# -*- coding: utf-8 -*-
"""
Created on Mon May  19  2025

@author: Krishna Murthy S (krishnamurthy.s@hpe.com)
"""
import threading
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas as pd

from Utilies.Client import Auth

'''importing libraries'''
import re
import csv
import os
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from os.path import join, exists, isdir, basename
from os import mkdir, listdir

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Sharepoint_List(Auth):

    def __init__(self, Auth):
        """
        Initialize SharePoint List instance with authentication token and account.
        """
        super().__init__(Auth)
        self.account = self.generate_token()
        self.account_scopes = {
            "send_mail": "email_send",
            "read_mail": "email_read",
            "sharepoint_read": "sharepoint_read",
            "sharepoint_write": "sharepoint_write",
            "graph_read": "graph_read",
            "graph_write": "graph_write",
            "teams_read": "teams_read",
            "teams_write": "teams_write",
            "exchange_read": "exchange_read"
        }

    def _get_sharepoint_instance(self, sharepoint_name, prefix='teams/', internal_site='hpe.sharepoint.com'):
        """
        Helper method to get the SharePoint instance and return site and list objects.
        """
        try:
            sharepoint_instance = self.account.sharepoint()
            site = sharepoint_instance.get_site(f'{internal_site}:/{prefix}/{sharepoint_name}')
            return site
        except Exception as e:
            logging.error(f"Error fetching SharePoint instance: {e}")
            return None

    def get_list_details(self, sharepoint_name, list_name, prefix='teams/', internal_site='hpe.sharepoint.com',
                         filters: dict = None, logic: str = 'and', contains: bool = False, limit: int = 0,
                         export_need=True, save_details=None):
        """
        Fetch details from a SharePoint list based on the filters, logic, and other parameters.
        Handles pagination if more than 200 items are present.
        """
        if not sharepoint_name:
            raise ValueError("Sharepoint name cannot be empty.")

        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            logging.error(f"Site '{sharepoint_name}' not found.")
            return []

        sp_list = site.get_list_by_name(list_name)

        if not sp_list:
            logging.error(f"List '{list_name}' not found.")
            return []

        field_map = {col.internal_name: col.display_name for col in sp_list.get_list_columns() if
                     col.internal_name and hasattr(col, 'display_name')}

        # Base URL
        url = f"https://graph.microsoft.com/v1.0/sites/{site.object_id}/lists/{sp_list.object_id}/items"
        filter_clauses = []

        # Build filter clauses based on provided filters
        if filters:
            for key, value in filters.items():
                if key.lower() == 'id':
                    url = f"https://graph.microsoft.com/v1.0/sites/{site.object_id}/lists/{sp_list.object_id}/items/{str(value)}"
                    break
                elif key in field_map:
                    if isinstance(value, str) and contains:
                        clause = f"contains(fields/{key}, '{value}')"
                    else:
                        clause = f"fields/{key} eq '{value}'"
                    filter_clauses.append(clause)
                else:
                    logging.warning(f"Field '{key}' not found in list schema. Skipping.")

        # Join filter clauses
        filter_string = f' {logic} '.join(filter_clauses) if filter_clauses else None

        # Prepare request parameters
        params = {'$expand': 'fields'}
        if filter_string:
            params['$filter'] = filter_string
        if limit > 0:
            params['$top'] = limit  # Optional: Respect limit if passed

        headers = {'Prefer': 'HonorNonIndexedQueriesWarningMayFailRandomly'}

        try:
            result = []
            response = sp_list.con.get(url, params=params, headers=headers)

            while True:
                response.raise_for_status()  # Will raise exception for 4xx/5xx HTTP errors
                data = response.json()

                # Single item case (e.g., /items/5)
                if filters and 'id' in [str(key).lower() for key in filters.keys()]:
                    item = data.get('fields', {})
                    return [item]

                items = data.get('value', [])
                if items:
                    result.extend([item.get('fields') for item in items])

                # Handle pagination, fetching next set of items if available
                next_link = data.get('@odata.nextLink')
                if next_link:
                    response = sp_list.con.get(next_link, headers=headers)
                else:
                    break

                # If a limit is set and we reach it, stop and return the results
                if limit > 0 and len(result) >= limit:
                    return result[:limit]

            if export_need:
                save_dir = save_details.get("save_dir", "exported_lists") if save_details else "exported_lists"
                save_type = save_details.get("save_type", "json").lower() if save_details else "json"
                safe_name = list_name.replace(" ", "_")
                filepath = os.path.join(save_dir, f"{safe_name}")

                # Get column display names from SharePoint
                try:
                    column_map = {
                        col.internal_name: col.display_name
                        for col in sp_list.get_list_columns()
                        if hasattr(col, 'display_name') and col.display_name
                    }
                except Exception as e:
                    logging.warning(f"Could not fetch column mappings for {list_name}: {e}")
                    column_map = {}

                # Transform data to use display names
                display_data = []
                for item in result:
                    display_item = {
                        column_map.get(key, key): value
                        for key, value in item.items()
                    }
                    display_data.append(display_item)

                # JSON Export
                if save_type == 'json':
                    with open(f"{filepath}.json", 'w', encoding='utf-8') as f:
                        json.dump(display_data, f, indent=2)

                # CSV Export
                elif save_type == 'csv':
                    if display_data:
                        keys = display_data[0].keys()
                        with open(f"{filepath}.csv", 'w', newline='', encoding='utf-8') as f:
                            writer = csv.DictWriter(f, fieldnames=keys)
                            writer.writeheader()
                            writer.writerows(display_data)

                # Excel Export
                elif save_type in ('excel', 'xlsx'):
                    if display_data:
                        df = pd.DataFrame(display_data)
                        df.to_excel(f"{filepath}.xlsx", index=False)

            return result

        except Exception as e:
            logging.error(f"Failed to fetch SharePoint list items: {e}")
            return []

    def create_list_item(self, sharepoint_name, list_name, item_data, prefix='teams/',
                         internal_site='hpe.sharepoint.com'):
        """
        Create a new item in a SharePoint list.
        """
        if not item_data:
            logging.error("Item data cannot be empty.")
            return

        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            logging.error(f"Site '{sharepoint_name}' not found.")
            return

        sp_list = site.get_list_by_name(list_name)
        if not sp_list:
            logging.error(f"List '{list_name}' not found.")
            return

        field_map = {col.internal_name: col.display_name for col in sp_list.get_list_columns() if
                     col.internal_name and hasattr(col, 'display_name')}

        # Filter the item data to ensure only valid fields are added
        filtered_item_data = {key: value for key, value in item_data.items() if key in field_map}

        if not filtered_item_data:
            logging.error("No valid fields to create the item.")
            return

        try:
            sp_list.create_list_item(filtered_item_data)
            logging.info(f"Item created in '{list_name}' list.")
        except Exception as e:
            logging.error(f"Failed to create item: {e}")

    def read_list_items(self, sharepoint_name, list_name, prefix='teams/', internal_site='hpe.sharepoint.com'):
        """
        Read all items from a SharePoint list.
        """
        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            logging.error(f"Site '{sharepoint_name}' not found.")
            return []

        sp_list = site.get_list_by_name(list_name)
        if not sp_list:
            logging.error(f"List '{list_name}' not found.")
            return []

        try:
            items = sp_list.get_items()
            return items
        except Exception as e:
            logging.error(f"Failed to fetch list items: {e}")
            return []

    def update_list_item(self, sharepoint_name, list_name, item_id, updated_data, prefix='teams/',
                         internal_site='hpe.sharepoint.com'):
        """
        Update an existing item in a SharePoint list.
        """
        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            logging.error(f"Site '{sharepoint_name}' not found.")
            print(f"Site '{sharepoint_name}' not found.")
            return

        sp_list = site.get_list_by_name(list_name)
        if not sp_list:
            logging.error(f"List '{list_name}' not found.")
            print(f"List '{list_name}' not found.")
            return

        item = sp_list.get_item_by_id(item_id)
        if not item:
            logging.error(f"Item with ID {item_id} not found.")
            print(f"Item with ID {item_id} not found.")
            return

        try:
            item.update_fields(updated_data)
            item.save_updates()
            logging.info(f"Item with ID {item_id} updated.")
            print(f"Item with ID {item_id} updated.")
        except Exception as e:
            logging.error(f"Failed to update item: {e}")
            print(f"Failed to update item: {e}")

    def delete_list_item(self, sharepoint_name, list_name, item_id, prefix='teams/',
                         internal_site='hpe.sharepoint.com'):
        """
        Delete an item from a SharePoint list.
        """
        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            logging.error(f"Site '{sharepoint_name}' not found.")
            print(f"Site '{sharepoint_name}' not found.")
            return

        sp_list = site.get_list_by_name(list_name)
        if not sp_list:
            logging.error(f"List '{list_name}' not found.")
            print(f"List '{list_name}' not found.")
            return

        item = sp_list.get_item_by_id(item_id)
        if not item:
            logging.error(f"Item with ID {item_id} not found.")
            print(f"Item with ID {item_id} not found.")
            return

        try:
            item.delete()
            logging.info(f"Item with ID {item_id} deleted.")
            print(f"Item with ID {item_id} deleted.")
        except Exception as e:
            logging.error(f"Failed to delete item: {e}")
            print(f"Failed to delete item: {e}")

    def get_list_schema(self, sharepoint_name, list_name, prefix='teams/', internal_site='hpe.sharepoint.com'):
        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            return []

        sp_list = site.get_list_by_name(list_name)
        columns = sp_list.get_list_columns()
        return [{
            'internal_name': col.internal_name,
            'display_name': getattr(col, 'display_name', col.internal_name),
            'type': col.field_type,
            'required': col.required,
            'hidden': col.hidden,
            'indexed': col.indexed
        } for col in columns]

    def download_all_site_lists(self, sharepoint_name, prefix='teams/', internal_site='hpe.sharepoint.com',
                                export_need=True, save_details=None):
        logging.info(f"Initializing download of all SharePoint lists from site: {sharepoint_name}")
        print(f"Initializing download of all SharePoint lists from site: {sharepoint_name}")

        site = self._get_sharepoint_instance(sharepoint_name, prefix, internal_site)
        if not site:
            logging.error("Site not found. Exiting download.")
            print("Site not found. Exiting download.")
            return {}

        save_dir = save_details.get("save_dir", "exported_lists") if save_details else "exported_lists"
        save_type = save_details.get("save_type", "json").lower() if save_details else "json"

        os.makedirs(save_dir, exist_ok=True)
        logging.info(f"Data will be saved to '{save_dir}' as '{save_type.upper()}' format.")
        print(f"Data will be saved to '{save_dir}' as '{save_type.upper()}' format.")

        try:
            lists = site.get_lists()
            logging.info(f"Found {len(lists)} lists on the site.")
            print(f"Found {len(lists)} lists on the site.")

            all_data = {}

            def fetch_and_export(sp_list):
                list_name = sp_list.name
                logging.info(f"[Start] Fetching data for list: {list_name}")
                print(f"[Start] Fetching data for list: {list_name}")

                list_data = []
                url = f"https://graph.microsoft.com/v1.0/sites/{site.object_id}/lists/{sp_list.object_id}/items"
                params = {'$expand': 'fields'}
                headers = {'Prefer': 'HonorNonIndexedQueriesWarningMayFailRandomly'}

                try:
                    response = sp_list.con.get(url, params=params, headers=headers)
                    while True:
                        response.raise_for_status()
                        data = response.json()
                        items = data.get('value', [])
                        list_data.extend([item.get('fields') for item in items])

                        next_link = data.get('@odata.nextLink')
                        if not next_link:
                            break
                        logging.info(f"Fetching next page for list: {list_name}")
                        print(f"Fetching next page for list: {list_name}")
                        response = sp_list.con.get(next_link, headers=headers)

                    if export_need:
                        safe_name = list_name.replace(" ", "_")
                        filepath = os.path.join(save_dir, f"{safe_name}")

                        try:
                            column_map = {
                                col.internal_name: col.display_name
                                for col in sp_list.get_list_columns()
                                if hasattr(col, 'display_name') and col.display_name
                            }
                            logging.info(f"Fetched column mappings for list: {list_name}")
                            print(f"Fetched column mappings for list: {list_name}")
                        except Exception as e:
                            logging.warning(f"Could not fetch column mappings for {list_name}: {e}")
                            print(f"Could not fetch column mappings for {list_name}: {e}")
                            column_map = {}

                        display_data = []
                        for item in list_data:
                            display_item = {
                                column_map.get(key, key): value
                                for key, value in item.items()
                            }
                            display_data.append(display_item)

                        try:
                            if save_type == 'json':
                                with open(f"{filepath}.json", 'w', encoding='utf-8') as f:
                                    json.dump(display_data, f, indent=2)
                                logging.info(f"Exported '{list_name}' to JSON: {filepath}.json")
                                print(f"Exported '{list_name}' to JSON: {filepath}.json")

                            elif save_type == 'csv':
                                if display_data:
                                    keys = display_data[0].keys()
                                    with open(f"{filepath}.csv", 'w', newline='', encoding='utf-8') as f:
                                        writer = csv.DictWriter(f, fieldnames=keys)
                                        writer.writeheader()
                                        writer.writerows(display_data)
                                    logging.info(f"Exported '{list_name}' to CSV: {filepath}.csv")
                                    print(f"Exported '{list_name}' to CSV: {filepath}.csv")

                            elif save_type in ('excel', 'xlsx'):
                                if display_data:
                                    df = pd.DataFrame(display_data)
                                    df.to_excel(f"{filepath}.xlsx", index=False)
                                    logging.info(f"Exported '{list_name}' to Excel: {filepath}.xlsx")
                                    print(f"Exported '{list_name}' to Excel: {filepath}.xlsx")

                        except Exception as e:
                            logging.error(f"Failed to export list '{list_name}': {e}")
                            print(f"Failed to export list '{list_name}': {e}")

                    return (list_name, list_data)

                except Exception as e:
                    logging.error(f"Error processing list '{list_name}': {e}")
                    print(f"Error processing list '{list_name}': {e}")
                    return (list_name, [])

            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(fetch_and_export, sp_list) for sp_list in lists]

                for future in as_completed(futures):
                    list_name, data = future.result()
                    all_data[list_name] = data
                    logging.info(f"[Done] Finished processing list: {list_name} ({len(data)} items)")
                    print(f"[Done] Finished processing list: {list_name} ({len(data)} items)")

            logging.info("All lists downloaded and exported successfully.")
            print("All lists downloaded and exported successfully.")
            return all_data

        except Exception as e:
            logging.error(f"Failed to fetch all lists: {e}")
            print(f"Failed to fetch all lists: {e}")
            return {}


class SharePointManager(Auth):

    def __init__(self,Auth):
        """
        Initialize SharePoint List instance with authentication token and account.
        """
        super().__init__(Auth)
        self.acnt = self.generate_token()
        self.account_scopes = {
            "sharepoint_read": "sharepoint_read",
            "sharepoint_write": "sharepoint_write",
            "graph_read": "graph_read",
            "graph_write": "graph_write",
            "exchange_read": "exchange_read"
        }

    def get_site(self, site_name, resource=None, library_name='default', prefix='teams/', domain='hpe.sharepoint.com'):
        if prefix not in site_name:
            site_name = "/" + prefix + site_name
        sp = self.acnt.sharepoint()
        if resource:
            sp = self.acnt.sharepoint(resource=resource)
        site = sp.get_site(domain, site_name)

        if library_name != 'default':
            for lib in site.list_document_libraries():
                if lib.name.lower() == library_name.lower():
                    return lib.get_root_folder()
            raise Exception("Document Library not found")
        return site.get_default_document_library().get_root_folder()

    def get_item_by_path(self, root_folder, path_parts):
        if isinstance(path_parts, str):
            path_parts = path_parts.strip('\\').split('\\')

        current = root_folder
        for part in path_parts:
            match = next((item for item in current.get_items() if item.name == part), None)
            if not match:
                return None
            current = match
        return current

    def download_item(self, item, local_path):
        if item.is_folder:
            target_path = join(local_path, item.name)
            if not exists(target_path):
                mkdir(target_path)
            item.download_contents(target_path)
        else:
            item.download(local_path)

    def upload_item(self, local_path, destination_folder):
        if not isdir(local_path):
            destination_folder.upload_file(local_path)
        else:
            folder = self._create_or_get_folder(destination_folder, basename(local_path))
            for entry in listdir(local_path):
                full_path = join(local_path, entry)
                self.upload_item(full_path, folder)

    def _create_or_get_folder(self, parent_folder, folder_name, if_exists='replace'):
        existing = [f for f in parent_folder.get_items() if f.name == folder_name and f.is_folder]
        if existing:
            if if_exists == 'replace':
                existing[0].delete()
                return parent_folder.create_child_folder(folder_name)
            elif if_exists == 'create_copy':
                new_name = folder_name
                counter = 1
                while any(f.name == new_name for f in parent_folder.get_items()):
                    new_name = f"{folder_name} ({counter})"
                    counter += 1
                return parent_folder.create_child_folder(new_name)
            else:
                return existing[0]
        return parent_folder.create_child_folder(folder_name)

    def download_filtered_files(self, site_name, root_folder_path, local_download_path, filters=None,
                                library_name='Documents', download_folder=False):
        """
        Downloads filtered files from a SharePoint folder path recursively.
        :param site_name: SharePoint site (e.g. 'Developedcodes')
        :param root_folder_path: Path in document library (e.g. 'Krishna_Test_folder')
        :param local_download_path: Local path to save files
        :param filters: Optional dictionary of filters
        :param library_name: Document library name (e.g. 'Documents')
        """
        if filters is None:
            filters = {}

        # Step 1: Get SharePoint site
        sp_site = self.acnt.sharepoint().get_site('hpe.sharepoint.com', f'teams/{site_name}')

        # Step 2: Get document library
        libraries = sp_site.list_document_libraries()
        drive = None
        for lib in libraries:
            if lib.name.lower() == library_name.lower():
                drive = lib
                break

        if drive is None:
            raise Exception(f"Document library '{library_name}' not found in site '{site_name}'")

        # Step 3: Get folder object by path
        root_folder = drive.get_item_by_path(root_folder_path)

        # Step 4: Start recursive download
        if not os.path.exists(local_download_path):
            os.makedirs(local_download_path)

        self._download_from_folder_object(root_folder, local_download_path, filters, download_folder)

    def _download_from_folder_object(self, folder_obj, local_path, filters, download_folder):
        """
        Recursively download files from a folder object using filters and threads for subfolders.
        """
        threads = []

        for item in folder_obj.get_items():
            item_name = item.name
            item_local_path = os.path.join(local_path, item_name)
            if not self.matches_filters(item_name, item, filters) and item.is_folder and download_folder:
                file_names = [item.name for item in item.get_items()]
                for files_name in file_names:
                    print(f"Downloading {files_name} in {item_name}")
                item.download_contents(item_local_path)
            elif item.is_folder and download_folder == False:
                if not os.path.exists(item_local_path):
                    os.makedirs(item_local_path)

                # Create thread for subfolder download
                t = threading.Thread(
                    target=self._download_from_folder_object,
                    args=(item, item_local_path, filters,download_folder)
                )
                t.start()
                threads.append(t)

            if not download_folder:
                # Apply filters
                if self.matches_filters(item_name, item, filters):
                    print(f"[Skipping] {item_name}")
                    continue

                if not os.path.exists(local_path):
                    os.makedirs(local_path)

                try:
                    print(f"[Downloading] {item_name}")
                    item.download(local_path)
                    print(f"[Downloaded] {item_name} to {local_path}")
                except Exception as e:
                    print(f"[Error] Failed to download {item_name}: {e}")

        # Wait for all threads to complete
        for t in threads:
            t.join()

    @dataclass
    class FileInfo:
        name: str
        full_path: str
        size: int
        created: datetime
        modified: datetime
        accessed: datetime
        mime_type: Optional[str] = None
        parent_path: Optional[str] = None

    def build_file_info(self, file_path: str) -> "SharePointManager.FileInfo":
        stats = os.stat(file_path)
        return self.FileInfo(
            name=os.path.basename(file_path),
            full_path=file_path,
            size=stats.st_size,
            created=datetime.fromtimestamp(stats.st_ctime),
            modified=datetime.fromtimestamp(stats.st_mtime),
            accessed=datetime.fromtimestamp(stats.st_atime),
            parent_path=os.path.dirname(file_path)
        )

    def matches_filters(self, filename, file_info, filters):
        """
        Determines if the given file matches the specified filters.

        :param filename: string (filename)
        :param file_info: object with 'created', 'modified', 'accessed' as datetime objects, and additional file details
        :param filters: dictionary with filter rules
        :return: True if file should be skipped (i.e., doesn't match filter), False otherwise
        """
        filename_lower = filename.lower()

        # Starts/Ends with
        if 'starts_with' in filters:
            values = filters['starts_with'].split(';')
            if not any(filename_lower.startswith(str(v).lower()) for v in values):
                return True

        if 'ends_with' in filters:
            values = filters['ends_with'].split(';')
            if not any(filename_lower.endswith(str(v).lower()) for v in values):
                return True

        if 'contains' in filters:
            values = filters['contains'].split(';')
            if not any(str(v).lower() in filename_lower for v in values):
                return True

        if 'not_contains' in filters:
            values = filters['not_contains'].split(';')
            if any(str(v).lower() in filename_lower for v in values):
                return True

        if 'not_extension' in filters:
            values = filters['not_extension'].split(';')
            if any(filename_lower.endswith(ext.lower()) for ext in values):
                return True

        if 'not_regex' in filters:
            values = filters['not_regex'].split(';')
            if any(re.search(regex, filename, re.IGNORECASE) for regex in values):
                return True

        # File size filters
        if 'size_greater_than' in filters:
            if file_info.size <= filters['size_greater_than']:
                return True

        if 'size_less_than' in filters:
            if file_info.size >= filters['size_less_than']:
                return True

        # Mime Type
        if 'mime_type' in filters:
            if file_info.mime_type.lower() != filters['mime_type'].lower():
                return True

        # Parent folder name match
        if 'parent_folder' in filters:
            parent_folder = file_info.parent_path.split('/')[-1].lower()
            if parent_folder != filters['parent_folder'].lower():
                return True

        if 'path_contains' in filters:
            if filters['path_contains'].lower() not in file_info.parent_path.lower():
                return True

        # Date-based filters
        ctime = file_info.created
        if 'created_after' in filters and ctime < filters['created_after']:
            return True
        if 'created_before' in filters and ctime > filters['created_before']:
            return True

        mtime = file_info.modified
        if 'modified_after' in filters and mtime < filters['modified_after']:
            return True
        if 'modified_before' in filters and mtime > filters['modified_before']:
            return True

        if 'modified_within_days' in filters:
            delta = datetime.now() - mtime
            if delta.days > filters['modified_within_days']:
                return True

        # Custom callable filter
        if 'custom_filter' in filters and callable(filters['custom_filter']):
            if not filters['custom_filter'](filename, file_info):
                return True

        return False

    def download_specific_file(self, site_name, file_path_on_sharepoint, local_download_folder,
                               library_name='Documents', prefix='teams/', domain='hpe.sharepoint.com'):
        """
        Downloads a specific file from SharePoint to a local folder.

        :param site_name: The SharePoint site name (e.g. 'yoursite')
        :param library_name: The document library name (e.g. 'Documents')
        :param file_path_on_sharepoint: The full path to the file in SharePoint (e.g. 'Folder/Subfolder/filename.ext')
        :param local_download_folder: Local folder to download the file into
        :param credentials: Tuple of (client_id, client_secret)
        """

        # Step 1: Get SharePoint site
        sp_site = self.acnt.sharepoint().get_site(domain, f'{prefix}{site_name}')

        # Step 2: Get document library
        libraries = sp_site.list_document_libraries()
        drive = None
        for lib in libraries:
            if lib.name.lower() == library_name.lower():
                drive = lib
                break

        if drive is None:
            raise Exception(f"Document library '{library_name}' not found in site '{site_name}'")

        # Clean up the path for SharePoint
        file_path_on_sharepoint = file_path_on_sharepoint.replace('\\', '/')

        item = drive.get_item_by_path(file_path_on_sharepoint)

        if item is None:
            raise Exception(f"The item at path '{file_path_on_sharepoint}' was not found.")

        if not item.is_file:
            raise Exception(f"The path '{file_path_on_sharepoint}' is a folder, not a file.")
        print(f"[Downloading] {item.name}")
        item.download(local_download_folder)
        print(f"[Downloaded] {item.name} to {local_download_folder}")

    def upload_filtered_files(self, site_name, library_name, sharepoint_target_path, local_folder_path, filters=None,
                              prefix='teams/', domain='hpe.sharepoint.com'):
        """
        Upload files from local folder to SharePoint folder, applying filters.

        :param site_name: SharePoint team site name (e.g. 'Developedcodes')
        :param library_name: Document library (e.g. 'Documents')
        :param sharepoint_target_path: Target path on SharePoint (e.g. 'Folder/Subfolder')
        :param local_folder_path: Local folder to read files from
        :param filters: Dictionary of filters to apply before uploading
        """
        if filters is None:
            filters = {}

        # Normalize path
        sharepoint_target_path = sharepoint_target_path.replace("\\", "/")

        # Step 1: Connect to site
        sp_site = self.acnt.sharepoint().get_site(domain, f'{prefix}{site_name}')

        # Step 2: Get correct document library
        drive = None
        for lib in sp_site.list_document_libraries():
            if lib.name.lower() == library_name.lower():
                drive = lib
                break
        if drive is None:
            raise Exception(f"Document library '{library_name}' not found.")

        # Step 3: Navigate to target folder
        target_folder = drive.get_item_by_path(sharepoint_target_path)

        # Step 4: Walk through local files
        for root, _, files in os.walk(local_folder_path):
            for file in files:

                full_path = os.path.join(root, file)
                file_info = self.build_file_info(full_path)
                # Apply filters
                if self.matches_filters(file_info.name, file_info, filters):
                    print(f"[Skipping] {file}")
                    continue

                rel_path = os.path.relpath(full_path, local_folder_path).replace("\\", "/")
                sp_folder_path = os.path.dirname(rel_path)

                current_folder = target_folder
                if sp_folder_path and sp_folder_path != " ":

                    for part in sp_folder_path.strip("/").split("/"):
                        found = False
                        for child in current_folder.get_child_folders():
                            if child.name == part:
                                print(f"[Info] Found existing folder: {part}")
                                current_folder = child
                                found = True
                                break
                        if not found:
                            print(f"[Info] Creating folder: {part}")
                            current_folder = current_folder.create_child_folder(part)
                current_folder.upload_file(item=full_path)
                print(f"[Uploaded] {rel_path}")
