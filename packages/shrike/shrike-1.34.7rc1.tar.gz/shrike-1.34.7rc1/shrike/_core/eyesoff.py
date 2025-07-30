# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json
from hashlib import sha256


# This list is up-to-date as of 03/23/2022.
# Contact aims-team@microsoft.com if your eyes-on subscription is not included.
EYES_ON_SUBSCRIPTIONS = set(
    [
        "d3259042d8e1f4f5b44ac56c9ca150955cd6a48d22180cf15f37133b850f784e",
        "887f1c5c3f867712fb0cd743e67325643e95a4c29954bce9ebef08922749daf1",
        "dfcaf96e30a340fae2fcd5871a5e94cf3805f6521d5e2571d55b097df857c9c3",
        "89b8bdaf7904e676c93e24be918b83c64fe904a4097821e3def68c0c33d1599b",
        "7f4ce25ded92373dd8ee223d40133e33632601866a7a035c050c13998098bf3b",
        "897107fb585b318ffa494339fd6bd5c38e96548c90c8809d8522c6e71b471cad",
        "e93b407a7a2b559f2cd8ea67d9a1bffbbbca1f616bd47347aea299a993bb4120",
        "71adef91aa2cb4676d995e8b3843dfe75d65e200dd8b552e0c7f5195c043f946",
        "2585e2381d1a9a413392c6c5372ca0bafdb845de17f0bfb5536d340401dee699",
        "7f6d1d5c3d3f46b0459bbb041e6ebebcfceff2e202aa02cb23301761e51b9c0b",
        "d675de4926b9534967be30a8cb035cb3d14b2d02b00ca3077d451a48910841ac",
        "84631d56ce357894baa249912456077e15f899c16639cdaef8c531013990db87",
        "566032778897f87065c0fab68a33e8b184e23a007d392f5a71dbb5f46bf2c460",
        "7141d27136d73133d699a94ebb36d29b524767949c07ba175d265420792b8448",
        "544181f90401adb3bfe691467fdd8dfd37b2eb689b15bcc8585adc6bb81df5d0",
        "9ad143f7e6c66dfa1fa39f147ed258fd584e05792b11a7dd3600537e28e39191",
        "f438a35eb69dd495c8ccb75cf6e554da2ab772ea923b801c822a64b3d43c0926",
        "0e977328631074f17aedfeec10ed487ff71231501357b5eb8b9c454a5604adf0",
        "8776711f970cd8aa00047879e5bee9ba9a0a9a0890241cb5ebd94a7173563bad",
        "d2e95d22a8e429f4e5b6291f3daa0cee13b518241ad30d3f159f9fd242ec7df9",
        "9fe3e3bd8dfdcd3e707c6840161d625460703d8e1e779b8b0e4965f7b1d17d6c",
        "d194e7433fdc4e28c33fd17cdb42db67fd84d0728f9471ad106b8c4f08fa78ff",
        "770f1203c522f031dde28fab282ee3fbdeb62afa05d3792610254e97171828c5",
        "0ed8ac8b95eaaa98425aee7c3d5500307c4aa1451e19a89853f244b061c93211",
        # MS Digital PPE c9e22707-27bc-4418-9161-d43db1d1ecde
        "5228efa9c19f997a585adf0cd32136afdaa6fb33a212524a38f801eb49e6170e",
        # MS Digital PROD 08047947-f71e-4462-a09d-266e3d34c431
        "b56e2a62d02e8d93375c07b37d079e1be5593c34cbdd489c0c7e050c217aa4e9",
    ]
)
EYES_OFF_TENANT_ID = "cdc5aeea-15c5-4db6-b079-fcadd2505dc2"

POLYMER_FEED = "--index-url https://o365exchange.pkgs.visualstudio.com/_packaging/PolymerPythonPackages/pypi/simple/"  # noqa: E501
O365_FEED = "--index-url https://o365exchange.pkgs.visualstudio.com/_packaging/O365PythonPackagesV2/pypi/simple/"  # noqa: E501


def get_hashed_eyes_on_subs():
    """
    This method is used to generated EYES_ON_SUBSCRIPTIONS.
    """
    with open("torus_subscription.json", "r") as f:
        # get torus_subscription.json from https://resources.azure.com/subscriptions with torus account  # noqa: E501
        all_info = json.load(f)
    all_sub = []
    for i in all_info["value"]:
        all_sub.append(i["subscriptionId"].lower())

    # Heron known eyes-off subscriptions: MOP/MDP sandboxes in the following list
    # https://eng.ms/docs/experiences-devices/m365-core/microsoft-search-assistants-intelligence-msai/substrate-intelligence/ai-training-heron/documentation/subscriptions  # noqa: E501
    eyes_off_sub = [
        "08047947-f71e-4462-a09d-266e3d34c431",  # MOP PROD
        "60d27411-7736-4355-ac95-ac033929fe9d",  # MOP PROD
        "2dea9532-70d2-472d-8ebd-6f53149ad551",  # MOP PROD
        "a6d8cf0d-b71e-4ffe-9a03-3e6013fed98a",  # MOP PPE
        "ecd580b4-55ff-46a9-b6e8-f7fabf1e4f8f",  # MOP INT
        "22ee5670-a769-4d11-9ba6-246a73123831",  # MDP INT
        "af1d7d72-11ca-495f-909f-7e91c65d7e22",  # MDP PPE
        "8987c30c-7019-4ef5-8214-d1e94c0abeb4",  # MDP PROD
    ]

    eyes_on_sub = []
    for i in all_sub:
        if i not in eyes_off_sub:
            eyes_on_sub.append(sha256(i.encode()).hexdigest())
    return eyes_on_sub


def is_eyesoff_helper(tenant_id, subscription_id):
    if tenant_id and tenant_id != EYES_OFF_TENANT_ID:
        # tenant_id could be None for HDI jobs
        return False
    else:
        hashed_subscription_id = sha256(subscription_id.encode()).hexdigest()
        return hashed_subscription_id not in EYES_ON_SUBSCRIPTIONS
