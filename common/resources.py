from enum import StrEnum


class BANK_NAMES(StrEnum):
    AL_KHARID_PVP_CHESTS = "AL_KHARID_PVP_CHESTS",
    AL_KHARID = "AL_KHARID",
    ARCEUUS = "ARCEUUS",
    ARDOUGNE_NORTH = "ARDOUGNE_NORTH",
    ARGOUDNE_SOUTH = "ARGOUDNE_SOUTH",
    BARBARIAN_OUTPOST = "BARBARIAN_OUTPOST",
    BLAST_FURNACE_BANK = "BLAST_FURNACE_BANK",
    BLAST_MINE = "BLAST_MINE",
    BURGH_DE_ROTT = "BURGH_DE_ROTT",
    CAMELOT = "CAMELOT",
    CANIFIS = "CANIFIS",
    CASTLE_WARS = "CASTLE_WARS",
    CATHERBY = "CATHERBY",
    DIHN_BANK = "DIHN_BANK",
    DRAYNOR = "DRAYNOR",
    DUEL_ARENA = "DUEL_ARENA",
    DWARF_MINE_BANK = "DWARF_MINE_BANK",
    EDGEVILLE = "EDGEVILLE",
    FALADOR_EAST = "FALADOR_EAST",
    FALADOR_WEST = "FALADOR_WEST",
    FARMING_GUILD = "FARMING_GUILD",
    FEROX_ENCLAVE = "FEROX_ENCLAVE",
    FISHING_GUILD = "FISHING_GUILD",
    FOSSIL_ISLAND = "FOSSIL_ISLAND",
    GNOME_BANK = "GNOME_BANK",
    GNOME_TREE_BANK_SOUTH = "GNOME_TREE_BANK_SOUTH",
    GNOME_TREE_BANK_WEST = "GNOME_TREE_BANK_WEST",
    GRAND_EXCHANGE = "GRAND_EXCHANGE",
    GREAT_KOUREND_CASTLE = "GREAT_KOUREND_CASTLE",
    HOSIDIUS = "HOSIDIUS",
    HOSIDIUS_KITCHEN = "HOSIDIUS_KITCHEN",
    JATIZSO = "JATIZSO",
    ISLE_OF_SOULS = "ISLE_OF_SOULS",
    LANDS_END = "LANDS_END",
    LOVAKENGJ = "LOVAKENGJ",
    LUMBRIDGE_BASEMENT = "LUMBRIDGE_BASEMENT",
    LUMBRIDGE_TOP = "LUMBRIDGE_TOP",
    LUNAR_ISLE = "LUNAR_ISLE",
    MOTHERLOAD = "MOTHERLOAD",
    MOUNT_KARUULM = "MOUNT_KARUULM",
    NARDAH = "NARDAH",
    NEITIZNOT = "NEITIZNOT",
    PEST_CONTROL = "PEST_CONTROL",
    PISCARILIUS = "PISCARILIUS",
    PRIFDDINAS = "PRIFDDINAS",
    ROGUES_DEN = "ROGUES_DEN",
    RUINS_OF_UNKAH = "RUINS_OF_UNKAH",
    SHANTY_PASS = "SHANTY_PASS",
    SHAYZIEN_BANK = "SHAYZIEN_BANK",
    SHAYZIEN_CHEST = "SHAYZIEN_CHEST",
    SHILO_VILLAGE = "SHILO_VILLAGE",
    SOPHANEM = "SOPHANEM",
    SULPHUR_MINE = "SULPHUR_MINE",
    TZHAAR = "TZHAAR",
    VARROCK_EAST = "VARROCK_EAST",
    VARROCK_WEST = "VARROCK_WEST",
    VINERY = "VINERY",
    VINERY_BANK = "VINERY_BANK",
    VOLCANO_BANK = "VOLCANO_BANK",
    WINTERTODT = "WINTERTODT",
    WOODCUTTING_GUILD = "WOODCUTTING_GUILD",
    YANILLE = "YANILLE",
    ZANARIS = "ZANARIS",
    ZEAH_SAND_BANK = "ZEAH_SAND_BANK",
    PORT_SARIM_DEPOSIT = "PORT_SARIM_DEPOSIT"


bank_locations = {
    BANK_NAMES.AL_KHARID: (3269, 3167, 0),
    BANK_NAMES.ARCEUUS: (1624, 3745, 0),
    BANK_NAMES.ARDOUGNE_NORTH: (2616, 3332, 0),
    BANK_NAMES.ARGOUDNE_SOUTH: (2655, 3283, 0),
    BANK_NAMES.BARBARIAN_OUTPOST: (2536, 3574, 0),
    BANK_NAMES.BLAST_FURNACE_BANK: (1948, 4957, 0),
    BANK_NAMES.BLAST_MINE: (1502, 3856, 0),
    BANK_NAMES.BURGH_DE_ROTT: (3495, 3212, 0),
    BANK_NAMES.CAMELOT: (2725, 3493, 0),
    BANK_NAMES.CANIFIS: (3512, 3480, 0),
    BANK_NAMES.CASTLE_WARS: (2443, 3083, 0),
    BANK_NAMES.CATHERBY: (2808, 3441, 0),
    BANK_NAMES.DIHN_BANK: (1640, 3944, 0),
    BANK_NAMES.DRAYNOR: (3092, 3243, 0),
    BANK_NAMES.DUEL_ARENA: (3381, 3268, 0),
    BANK_NAMES.DWARF_MINE_BANK: (2837, 10207, 0),
    BANK_NAMES.EDGEVILLE: (3094, 3492, 0),
    BANK_NAMES.FALADOR_EAST: (3013, 3355, 0),
    BANK_NAMES.FALADOR_WEST: (2946, 3368, 0),
    BANK_NAMES.FARMING_GUILD: (1253, 3741, 0),
    BANK_NAMES.FEROX_ENCLAVE: (3130, 3631, 0),
    BANK_NAMES.FISHING_GUILD: (2586, 3420, 0),
    BANK_NAMES.FOSSIL_ISLAND: (3739, 3804, 0),
    BANK_NAMES.GNOME_BANK: (2445, 3425, 1),
    BANK_NAMES.GNOME_TREE_BANK_SOUTH: (2449, 3482, 1),
    BANK_NAMES.GNOME_TREE_BANK_WEST: (2442, 3488, 1),
    BANK_NAMES.GRAND_EXCHANGE: (3164, 3487, 0),
    BANK_NAMES.GREAT_KOUREND_CASTLE: (1612, 3681, 2),
    BANK_NAMES.HOSIDIUS: (1749, 3599, 0),
    BANK_NAMES.HOSIDIUS_KITCHEN: (1676, 3617, 0),
    BANK_NAMES.JATIZSO: (2416, 3801, 0),
    BANK_NAMES.ISLE_OF_SOULS: (2212, 2859, 0),
    BANK_NAMES.LANDS_END: (1512, 3421, 0),
    BANK_NAMES.LOVAKENGJ: (1526, 3739, 0),
    BANK_NAMES.LUMBRIDGE_BASEMENT: (3218, 9623, 0),
    BANK_NAMES.LUMBRIDGE_TOP: (3208, 3220, 2),
    BANK_NAMES.LUNAR_ISLE: (2099, 3919, 0),
    BANK_NAMES.MOTHERLOAD: (3760, 5666, 0),
    BANK_NAMES.MOUNT_KARUULM: (1324, 3824, 0),
    BANK_NAMES.NARDAH: (3428, 2892, 0),
    BANK_NAMES.NEITIZNOT: (2337, 3807, 0),
    BANK_NAMES.PEST_CONTROL: (2667, 2653, 0),
    BANK_NAMES.PISCARILIUS: (1803, 3790, 0),
    BANK_NAMES.PRIFDDINAS: (3257, 6106, 0),
    BANK_NAMES.ROGUES_DEN: (3043, 4973, 1),
    BANK_NAMES.RUINS_OF_UNKAH: (3156, 2835, 0),
    BANK_NAMES.SHANTY_PASS: (3308, 3120, 0),
    BANK_NAMES.SHAYZIEN_CHEST: (1486, 3646, 0),
    BANK_NAMES.SHAYZIEN_BANK: (1488, 3592, 0),
    BANK_NAMES.SHILO_VILLAGE: (2852, 2954, 0),
    BANK_NAMES.SOPHANEM: (2799, 5169, 0),
    BANK_NAMES.SULPHUR_MINE: (1453, 3858, 0),
    BANK_NAMES.TZHAAR: (2446, 5178, 0),
    BANK_NAMES.VARROCK_EAST: (3253, 3420, 0),
    BANK_NAMES.VARROCK_WEST: (3185, 3441, 0),
    BANK_NAMES.VINERY: (1808, 3570, 0),
    BANK_NAMES.VINERY_BANK: (1809, 3566, 0),
    BANK_NAMES.VOLCANO_BANK: (3819, 3809, 0),
    BANK_NAMES.WINTERTODT: (1640, 3944, 0),
    BANK_NAMES.WOODCUTTING_GUILD: (1591, 3479, 0),
    BANK_NAMES.YANILLE: (2613, 3093, 0),
    BANK_NAMES.ZANARIS: (2383, 4458, 0),
    BANK_NAMES.ZEAH_SAND_BANK: (1719, 3465, 0),
    BANK_NAMES.PORT_SARIM_DEPOSIT: (3045, 3235, 0),
    BANK_NAMES.AL_KHARID_PVP_CHESTS: (3383, 3270, 0),
}

STAIRS_OBJECTS = {
    '16673': {'click': 'left', 'description': 'Third floor stairs Lumbridge Castle'},
    '16672': {'click': 'right', 'up': '2', 'down': '3', 'description': 'Second floor stairs Lumbridge Castle'},
    '16671': {'click': 'left', 'description': 'First floor stairs Lumbridge Castle'},
}

BANK_BOOTH_OBJECTS = {
    '18491': {'click': 'left', 'description': 'Bank booth Lumbridge Castle'},
    '10583': {'click': 'left', 'description': 'West Varrock bank booth'},
    '26254': {'click': 'left', 'description': 'Port Sarim bank deposit box'},
    '3194': {'click': 'left', 'description': 'AL_KHARID_PVP_CHESTS'},
}
