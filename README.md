## Python Package License Search
A simple Python application to understand how Python projects are licensed.

## Usage
The `src/license.py` uses the [GitHub REST API](https://docs.github.com/en/rest) to lookup the licenses used by Python projects. It works by starting with a seed project to get a list of Python packages to search and looks up their licenses. The license frequencies are reported to standard output.

To run the application:

* Create a `.env` file, which contains your GitHub [access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) and username. You can use the `.env.template` as an example. Note, you can still run the project without authentication, but you may need to increase `SLEEP_DURATION` to prevent being rate limited. 
* With GNU Make, run `make all`. That will take care of creating the virtual environment and running the `src/license.py` script.
* Without GNU Make, you'll need to use `requirements.txt` to create the virtual environment and run the `src/license.py` script.

Results are cached for convenience; you may need to delete that caching directory. Running `make clean` takes care of removing the cache directory.

## License
This project is distributed under the GNU General Public License. Please see `COPYING` for more information.
