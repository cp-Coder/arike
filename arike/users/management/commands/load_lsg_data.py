import glob
import json
from typing import Optional
from collections import defaultdict
from django.core.management.base import BaseCommand, CommandParser
from arike.users.models import LOCAL_BODY_CHOICES, District, LSG_Body, State

class Command(BaseCommand):
    help = "Loads Local Body data from a folder of JSONs"
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("folder", help="path to the folder of JSONs")

    def handle(self, *args, **options) -> Optional[str]:
        folder = options["folder"]
        counter = 0
        local_bodies = []

        # Creates a map with first char of readable value as key
        LOCAL_BODY_CHOICE_MAP = dict([(c[1][0], c[0]) for c in LOCAL_BODY_CHOICES])

        state = {}
        district = defaultdict(dict)

        def get_state_obj(state_name):
            if state_name in state:
                return state[state_name]
            state_obj = State.objects.filter(name=state_name).first()
            if not state_obj:
                print(f"Creating State {state_name}")
                state_obj = State(name=state_name)
                state_obj.save()
            state[state_name] = state_obj
            return state_obj

        def get_district_obj(district_name, state_name):
            state_obj = get_state_obj(state_name)
            if state_name in district:
                if district_name in district[state_name]:
                    return district[state_name][district_name]
            district_obj = District.objects.filter(name=district_name, state=state_obj).first()
            if not district_obj:
                if not district_name:
                    return None
                print(f"Creating District {district_name}")
                district_obj = District(name=district_name, state=state_obj)
                district_obj.save()
            district[state_name][district_name] = district_obj
            return district_obj

        def create_local_bodies(local_body_list):
            local_body_objs = []
            for lb in local_body_list:
                dist_obj = get_district_obj(lb["district"], lb["state"])
                if not dist_obj:
                    continue
                local_body_objs.append(
                    LSG_Body(
                        name=lb["name"],
                        district=dist_obj,
                        lsg_body_code=lb.get("localbody_code"),
                        kind=LOCAL_BODY_CHOICE_MAP.get(
                            (lb.get("localbody_code", " "))[0], LOCAL_BODY_CHOICES[-1][0]
                        ),
                    )
                )

            # Possible conflict is name uniqueness.
            # If there is a conflict, it means that the record already exists.
            # Hence, those records can be ignored using the `ignore_conflicts` flag
            LSG_Body.objects.bulk_create(local_body_objs, ignore_conflicts=True)

        for f in glob.glob(f"{folder}/*.json"):
            counter += 1
            with open(f"{f}", "r") as data_f:
                data = json.load(data_f)
                data.pop("wards", None)
                local_bodies.append(data)

            # Write every 1000 records
            if counter % 1000 == 0:
                create_local_bodies(local_bodies)
                local_bodies = []
                print(f"Completed: {counter}")

        if len(local_bodies) > 0:
            create_local_bodies(local_bodies)
