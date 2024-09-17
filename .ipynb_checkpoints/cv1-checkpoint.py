import os
import argparse
import h5py
from pyhdf.SD import SD, SDC

def hdf4_to_hdf5(hdf4_file, hdf5_file):
    # Open the HDF4 file
    hdf4 = SD(hdf4_file, SDC.READ)
    # Create an HDF5 file
    hdf5 = h5py.File(hdf5_file, 'w')

    # Iterate through datasets in the HDF4 file
    for dataset in hdf4.datasets():
        data = hdf4.select(dataset)[:]
        # Write the dataset to HDF5
        hdf5.create_dataset(dataset, data=data)

    hdf4.end()
    hdf5.close()

def convert_directory(input_directory, output_directory):
    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Loop through all .hdf files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith('.hdf'):
            hdf4_file = os.path.join(input_directory, filename)
            # Create the corresponding .h5 filename
            hdf5_file = os.path.join(output_directory, os.path.splitext(filename)[0] + '.h5')
            
            print(f"Converting {hdf4_file} to {hdf5_file}...")
            hdf4_to_hdf5(hdf4_file, hdf5_file)
            print(f"Finished converting {hdf4_file} to {hdf5_file}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert HDF4 files to HDF5 format.')
    parser.add_argument('input_directory', type=str, help='Path to the input directory containing HDF4 files.')
    parser.add_argument('output_directory', type=str, help='Path to the output directory where HDF5 files will be saved.')

    args = parser.parse_args()

    convert_directory(args.input_directory, args.output_directory)
