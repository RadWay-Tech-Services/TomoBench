import argparse
import h5py
import pathlib


def main(args):
    with h5py.File(args.hdf_file, "r+") as hdf_file:
        for entry in hdf_file:
            entry_group = hdf_file[entry]
            entry_group.attrs["NX_class"] = "NXentry"
            entry_group.attrs["default"] = "data"
            entry_group.attrs["definition"] = "NXtomo"
            entry_group.attrs["version"] = 1.3

            if not "data" in entry_group:
                data_group = entry_group.create_group("data")
            else:
                data_group = entry_group["data"]
            data_group.attrs["NX_class"] = "NXdata"
            data_group.attrs["SILX_style/axis_scale_types"] = ["linear", "linear"]
            data_group.attrs["signal"] = "data"
            if not "data" in data_group:
                data_group["data"] = h5py.ExternalLink(
                    filename=pathlib.Path(
                        entry_group["flyScanDetector"]["data"].file.filename
                    ).name,
                    path="/entry/data/data",
                )
            data_group["data"].attrs["interpretation"] = "image"
            if not "rotation_angle" in data_group:
                data_group["rotation_angle"] = entry_group["tomo_entry"]["sample"][
                    "rotation_angle"
                ]
            for key in entry_group["tomo_entry"]:
                if not key in entry_group:
                    entry_group[key] = entry_group["tomo_entry"][key]
            if not "detector" in entry_group["instrument"]:
                entry_group["instrument"]["detector"] = entry_group["tomo_entry"][
                    "instrument"
                ]["detector"]
        detector_group = entry_group["instrument"]["detector"]
        del detector_group["distance"]
        detector_group["distance"] = 0.01
        detector_group["distance"].attrs["units"] = "m"
        del detector_group["x_pixel_size"]
        detector_group["x_pixel_size"] = 0.000006
        detector_group["x_pixel_size"].attrs["units"] = "m"
        del detector_group["y_pixel_size"]
        detector_group["y_pixel_size"] = 0.000006
        detector_group["y_pixel_size"].attrs["units"] = "m"
        if not "image_key_control" in detector_group:
            detector_group["image_key_control"] = detector_group["image_key"]

        sample_group = entry_group["sample"]
        if "x_translation" in sample_group:
            del sample_group["x_translation"]
        if "y_translation" in sample_group:
            del sample_group["y_translation"]
        if "z_translation" in sample_group:
            del sample_group["z_translation"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--hdf-file", required=True)
    args = parser.parse_args()
    main(args)
