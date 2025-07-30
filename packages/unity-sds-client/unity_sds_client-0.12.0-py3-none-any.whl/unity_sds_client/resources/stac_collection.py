import os
from datetime import datetime, timezone
from typing import List, Union
from pathlib import Path
# stage_in packages
from unity_sds_client.resources.collection import Collection
# stage_out packages
from unity_sds_client.resources.dataset import Dataset
from unity_sds_client.resources.data_file import DataFile

class STACCollectionCreator:
    """
    A class to create STAC Collection objects from a list of files using PySTAC.
    Each file becomes a pystac.Item with the file as a pystac.Asset.
    """
    
    def __init__(self, collection_name: str, collection_id: str, output_stac_catalog: str):
        """
        Initialize the STAC Collection Creator.
        
        Args:
            collection_name: Name for the collection
            collection_id: Unique identifier for the collection
            output_stac_catalog: Path where STAC catalog will be saved
        """
        self.collection_id = collection_id
        self.collection_name = collection_name
        self.output_stac_catalog = output_stac_catalog
    
    def create_collection(self, 
                         file_paths: List[Union[str, Path]]) -> Collection:
        """
        Create a STAC Collection object from a list of files using Unity SDS.
        
        Args:
            file_paths: List of file paths to include in the collection
            
        Returns:
            Collection object
        """
        # Convert paths to Path objects for easier manipulation
        paths = [Path(p) for p in file_paths]
        
        # Create the collection
        collection = Collection(
            id=self.collection_id
        )
        
        # Create items for each file and add to collection
        for path in paths:
            file_name = os.path.basename(path)
            # Create a Dataset for the collection
            dataset_name = self.collection_name+'_'+file_name
            dataset = Dataset(
                name=dataset_name, # STAC JSON ID
                collection_id=self.collection_id, # STAC JSON Collection
                start_time=datetime.now().replace(tzinfo=timezone.utc).isoformat(), 
                end_time=datetime.now().replace(tzinfo=timezone.utc).isoformat(),
                creation_time=datetime.now().replace(tzinfo=timezone.utc).isoformat()
            )
            
            self._add_file_to_dataset(path, dataset)

            # When we run "to_stac" below, this file will be generated. 
            # This needs to be added to the stac file itself for future reference.
            self._add_file_to_dataset(Path(dataset_name + '.json'), dataset, "metadata")

            collection._datasets.append(dataset)
            
        return collection

    def _add_file_to_dataset(self, file_path: Path, dataset: Dataset, role: str = "data"):
        """Add a file to the dataset as a DataFile."""
        
        # Determine file type based on extension
        file_type = self._get_file_type(file_path)
        
        # Add the data file to the dataset
        dataset.add_data_file(DataFile(file_type, str(file_path), [role]))

    def _get_file_type(self, file_path: Path) -> str:
        """Determine file type based on file extension."""
        extension = file_path.suffix.lower()
        
        # Map extensions to file types
        type_map = {
            '.tif': 'image/tiff',
            '.tiff': 'image/tiff',
            '.nc': 'application/x-netcdf',
            '.hdf5': 'application/x-hdf5',
            '.h5': 'application/x-hdf5',
            '.json': 'application/json',
            '.geojson': 'application/geo+json',
            '.csv': 'text/csv',
            '.txt': 'text/plain',
            '.xml': 'application/xml',
            '.zip': 'application/zip',
            '.gz': 'application/gzip'
        }
        
        return type_map.get(extension, 'application/octet-stream')

    def create_collection_to_stac(self, file_paths: List[Union[str, Path]]) -> Collection:
        """
        Create a STAC Collection from file paths and save to STAC catalog.
        
        Args:
            file_paths: List of file paths to include
            
        Returns:
            Collection object
        """
        collection = self.create_collection(file_paths)
        Collection.to_stac(collection, self.output_stac_catalog)
        return collection


# Example usage
if __name__ == "__main__":
    # Example file paths
    example_files = [
        "/path/to/data1.tif",
        "/path/to/data2.nc",
        "/path/to/results.json"
    ]
    
    creator = STACCollectionCreator(
        collection_name="my-collection-name-test", 
        collection_id="my-processing-results-test", 
        output_stac_catalog="/Users/leebrian/github/test/output/"
    )
    collection = creator.create_collection_to_stac(example_files)
    
    # Access collection info
    print(f"Collection ID: {collection.collection_id}")
