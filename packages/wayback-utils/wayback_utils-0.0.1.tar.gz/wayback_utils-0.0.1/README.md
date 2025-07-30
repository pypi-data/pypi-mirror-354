wayback_utils.py

This module provides a Python interface to interact with the Wayback Machine web page archiving service (web.archive.org). It allows you to save URLs, check the status of archiving jobs, and verify if a URL has already been indexed.

Main classes:
-------------

- WayBackStatus: Represents the status of an archiving job.
- WayBackSave: Represents the response when requesting to archive a URL.
- WayBack: Main class to interact with the Wayback Machine API.

Basic usage:
------------

1. Initialize the WayBack class with your access keys:

    wb = WayBack(ACCESS_KEY="your_access_key", SECRET_KEY="your_secret_key")

2. Save a URL:

    result = wb.save("https://example.com")

3. Check the status of a job:

    status = wb.status(result.job_id)

4. Verify if a URL is already archived:

    is_indexed = wb.indexed("https://example.com")

Notes:
------

- You need valid access keys (ACCESS_KEY and SECRET_KEY) to use the archiving API.
- You can provide an on_confirmation callback function to save() to receive the final archiving status asynchronously.
- The module uses requests and threading.

License:
--------
MIT license.