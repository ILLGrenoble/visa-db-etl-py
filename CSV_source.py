import asyncio
import asyncpg
from datetime import datetime
from timeit import timeit

async def run():
    import loader
    import csv
    loader = loader.Loader(await asyncpg.connect(host="172.18.0.1", database="etl", user="etl", password="etl_password", server_settings={'search_path': "visa2"}))
    def load_csv(tablename):
        # be careful : if an unquoted field end with a \n, the parser will stop the line there, and probably fail to load the end of the line
        for line in csv.DictReader(open("./csv_data/" + tablename + ".csv", newline='')):
            keys = line.keys()
            for key in keys:
                if "date" in key or key == "activated_at":
                    try:
                        line[key] = datetime.strptime(line[key], "%Y-%m-%d %H:%M:%S.%f").date()
                    except ValueError:
                        line[key] = None
            yield line
            
    await loader.init_schema()

    await loader.clean()
    await loader.employer(load_csv("employer"))
    await loader.user(load_csv("user"))
    await loader.instrument(load_csv("instrument"))
    await loader.proposal(load_csv("proposal"))
    await loader.experiment(load_csv("experiment"))
    await loader.experiment_user(load_csv("experiment_user"))
    await loader.staff_user(load_csv("staff_user"))
    await loader.instrument_control_user(load_csv("instrument_control_user"))
    await loader.it_support_user(load_csv("it_support_user"))
    await loader.scientific_computing_user(load_csv("scientific_computing_user"))
    await loader.instrument_scientist(load_csv("instrument_scientist"))

asyncio.run(run())