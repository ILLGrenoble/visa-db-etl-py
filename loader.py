import re

class Loader():

    def __init__(self, conn):
        self.conn = conn
        self.parse_response_reg = re.compile("INSERT (\d) (\d)")

    async def init_schema(self):
        with open("schema.sql") as sql:
            print("Creating schema")
            res = await self.conn.execute(sql.read())
            print(res)

    async def clean(self):
        async with self.conn.transaction():
            await self.conn.execute("delete from instrument_scientist;")
            await self.conn.execute("delete from user_role where role_id = (select id from role where name = 'SCIENTIFIC_COMPUTING')")
            await self.conn.execute("delete from user_role where role_id = (select id from role where name = 'IT_SUPPORT')")
            await self.conn.execute("delete from user_role where role_id = (select id from role where name = 'INSTRUMENT_CONTROL')")
            await self.conn.execute("delete from user_role where role_id = (select id from role where name = 'STAFF')")
            await self.conn.execute("delete from experiment_user;")
            await self.conn.execute("delete from experiment where id not in (select distinct experiment_id from instance_experiment);")
            await self.conn.execute("delete from proposal where id not in (select distinct proposal_id from experiment);")
            await self.conn.execute("delete from instrument where id not in (select distinct instrument_id from experiment);")
            await self.conn.execute("delete from users where id not in (select distinct user_id from instance_command union select distinct user_id from instance_member union select distinct user_id from instance_session_member union select distinct user_id from user_role);")
            await self.conn.execute("delete from employer where id not in (select distinct affiliation_id from users);")
            print("everything cleaned")

    async def employer(self, employers):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for employer in employers:
                res = await self.conn.execute(
                    """INSERT INTO employer (id, name, town, country_code)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (id) DO UPDATE
                    SET name = $2, town=$3, country_code=$4""",
                    int(employer['id']),
                    employer['name'],
                    employer['town'],
                    employer['country_code']
                )
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Employer : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def experiment(self, experiments):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for experiment in experiments:
                res = await self.conn.execute(
                    """INSERT INTO experiment (id, proposal_id, instrument_id, start_date, end_date)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (id) DO UPDATE
                    SET proposal_id = $2, instrument_id=$3""",
                    experiment['id'],
                    int(experiment['proposal_id']),
                    int(experiment['instrument_id']),
                    experiment['start_date'],
                    experiment['end_date']
                )
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Experiment : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def experiment_user(self, exp_users):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for exp_user in exp_users:
                res = await self.conn.execute(
                    """INSERT INTO experiment_user (experiment_id, user_id)
                    VALUES ($1, $2) ON CONFLICT DO NOTHING""",
                    exp_user['experiment_id'],
                    exp_user['user_id'])
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Experiment User : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def instrument_control_user(self, ic_users):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0

            instrument_control_id = await self.conn.fetchval("select id from role where name = 'INSTRUMENT_CONTROL'")
            for ic_user in ic_users:
                res = await self.conn.execute(
                    """INSERT INTO user_role (user_id, role_id)
                    VALUES ($1, $2) ON CONFLICT DO NOTHING""",
                    ic_user['user_id'],
                    instrument_control_id)
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Instrument Control User : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def instrument(self, instruments):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for instrument in instruments:
                res = await self.conn.execute(
                    """INSERT INTO instrument (id, name)
                    VALUES ($1, $2)
                    ON CONFLICT (id) DO UPDATE
                    SET name = $2""",
                    int(instrument['id']),
                    instrument['name']
                )
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Instrument : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def instrument_scientist(self, instrument_scientists):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for instrument_scientist in instrument_scientists:
                res = await self.conn.execute(
                    """INSERT INTO instrument_scientist (instrument_id, user_id)
                    VALUES ($1, $2)
                    ON CONFLICT DO NOTHING""",
                    int(instrument_scientist['instrument_id']),
                    instrument_scientist['user_id']
                )
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Instrument responsible : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def it_support_user(self, it_support_users):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0

            it_support_id = await self.conn.fetchval("select id from role where name = 'IT_SUPPORT'")
            for it_support_user in it_support_users:
                res = await self.conn.execute(
                    """INSERT INTO user_role (user_id, role_id)
                    VALUES ($1, $2) ON CONFLICT DO NOTHING""",
                    it_support_user['user_id'],
                    it_support_id)
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("IT support User : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def proposal(self, proposals):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for proposal in proposals:
                res = await self.conn.execute(
                    """INSERT INTO proposal (id, identifier, title)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (id) DO UPDATE
                    SET identifier = $2, title = $3""",
                    int(proposal['id']),
                    proposal['identifier'],
                    proposal['title']
                )
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Proposal : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def scientific_computing_user(self, scientific_computing_user):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0

            scientific_computing_id = await self.conn.fetchval("select id from role where name = 'SCIENTIFIC_COMPUTING'")
            for scientific_computing_user in scientific_computing_user:
                res = await self.conn.execute(
                    """INSERT INTO user_role (user_id, role_id)
                    VALUES ($1, $2) ON CONFLICT DO NOTHING""",
                    scientific_computing_user['user_id'],
                    scientific_computing_id)
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Scientific computing User : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def staff_user(self, staff_users):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0

            staff_id = await self.conn.fetchval("select id from role where name = 'STAFF'")
            for staff_user in staff_users:
                res = await self.conn.execute(
                    """INSERT INTO user_role (user_id, role_id)
                    VALUES ($1, $2) ON CONFLICT DO NOTHING""",
                    staff_user['user_id'],
                    staff_id)
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("Staff User : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))

    async def user(self, users):
        async with self.conn.transaction():
            inserted = 0
            updated = 0
            total_lines = 0
            for user in users:
                res = await self.conn.execute(
                    """INSERT INTO users (id, first_name, last_name, email, affiliation_id, instance_quota, activated_at)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ON CONFLICT (id) DO UPDATE
                    SET first_name = $2, last_name = $3, email = $4, affiliation_id = $5, instance_quota = $6, activated_at = $7""",
                    user['id'],
                    user['first_name'],
                    user['last_name'],
                    user['email'],
                    int(user['affiliation_id'] or 0),
                    int(user['instance_quota']),
                    user['activated_at']
                )
                response_parsed = self.parse_response_reg.match(res)
                inserted  += int(response_parsed.group(1))
                updated += int(response_parsed.group(2))
                total_lines += 1
            print("User : INSERT {0} UPDATE {1} TOTAL {2}".format(inserted, updated, total_lines))
