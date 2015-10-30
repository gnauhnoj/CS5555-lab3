# CS5555 - Lab3

## Team Member(s): Jonathan Huang (jhh283)

This directory assumes that the data files are found in a data/ directory in root. It also assumes a config file which provide the following:
    - filemap - a dictionary mapping from fitbit datatype to file data/ filename (.json)
    - dataloader - a dictionary mapping from various required fields in data.py to their corresponding requirements. For example:
    ```json
    {
      'host': localhost for ohmage shimmer,
      'username': username,
      'shim': 'fitbit',
      'start': '2015-10-15',
      'normalize': 'false',
      'endpoints': ['activity', 'steps', 'weight', 'sleep']
    }
    ```

Fitbit data can be pulled using the script data.py script if the second config is provided.
