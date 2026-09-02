# Corpus metadata registry
# Each entry defines the bias context for a source document.
#
# bias_tag options:
#   none | indigenous_perspective | settler_bias | institutional_bias | neutral
#
# bias_level options:
#   none | mild | moderate | severe

CORPUS_REGISTRY = {
    # --- Tier 1: Primary Indigenous Sources ---
    "ethnography-of-owens-valley-paiute.pdf": {
        "tier": 1,
        "bias_tag": "academic",
        "bias_level": "mild",
        "description": (
            "Academic ethnography of Owens Valley Paiute by Julian Steward. "
            "Authoritative but filtered through an early to mid-20th century "
            "anthropological outside perspective."
        ),
    },
    "owens-valley-paiute-autobiographies.pdf": {
        "tier": 1,
        "bias_tag": "academic",
        "bias_level": "mild",
        "description": (
            "First-person Paiute autobiographies collected by Julian Steward. "
            "Primary indigenous voices but mediated by an outside academic collector."
        ),
    },
    "ov-native-water-story.pdf": {
        "tier": 1,
        "bias_tag": "primary_indigenous",
        "bias_level": "none",
        "description": (
            "Water story from Teri Red Owl, current head of the Owens Valley "
            "Indian Water Commission. Primary living indigenous voice on the "
            "water rights conflict and its ongoing impact."
        ),
    },
    "payahuunadu-oviwc.pdf": {
        "tier": 1,
        "bias_tag": "primary_indigenous",
        "bias_level": "none",
        "description": (
            "Owens Valley Indian Water Commission background on Payahǖǖnadǖ. "
            "Institutional indigenous voice on land and water rights."
        ),
    },
    "water-land-history-oviwc.pdf": {
        "tier": 1,
        "bias_tag": "primary_indigenous",
        "bias_level": "none",
        "description": (
            "Institutional indigenous perspective on the aqueduct conflict "
            "and its legacy."
        ),
    },

    # --- Tier 2: Period Primary and Local Sources ---
    "timeline-genocide-incidents-ov.pdf": {
        "tier": 2,
        "bias_tag": "none",
        "bias_level": "none",
        "description": (
            "Documented timeline of genocide incidents in the Owens Valley region."
        ),
    },
    "Ghosts-of-the-Sagebrush.pdf": {
        "tier": 2,
        "bias_tag": "none",
        "bias_level": "none",
        "description": (
            "Historical structures survey of the Mono Basin. Primarily a photo "
            "document with sparse descriptive text. Extracted text may be "
            "fragmentary — treat retrieved chunks as partial context only."
        ),
    },
    "fauna-flora-ov.pdf": {
        "tier": 2,
        "bias_tag": "none",
        "bias_level": "none",
        "description": (
            "Survey of indigenous, endemic, and endangered fauna and flora "
            "of the Owens Valley by Gigi de Jong."
        ),
    },

    # --- Tier 2: Chronicling America Newspapers ---
    "chronicling-america/indorse-owens-project-dec-25-1906.pdf": {
        "tier": 2,
        "bias_tag": "institutional_bias",
        "bias_level": "severe",
        "description": (
            "LA newspaper endorsing the Owens Valley water project, Dec 1906. "
            "Represents pro-aqueduct Los Angeles institutional perspective."
        ),
    },
    "chronicling-america/ov-aqueduct-city-growth-april-1-1906.pdf": {
        "tier": 2,
        "bias_tag": "institutional_bias",
        "bias_level": "severe",
        "description": (
            "LA newspaper on aqueduct and city growth, April 1906. "
            "Frames water acquisition as civic progress."
        ),
    },
    "chronicling-america/la-faces-water-crisis-july-31-1905.pdf": {
        "tier": 2,
        "bias_tag": "institutional_bias",
        "bias_level": "severe",
        "description": (
            "LA newspaper on water crisis, July 1905. "
            "Frames Owens Valley water as solution to LA's growth needs."
        ),
    },
    "chronicling-america/stealing-owens-river-supply-july-30-1905.pdf": {
        "tier": 2,
        "bias_tag": "institutional_bias",
        "bias_level": "severe",
        "description": (
            "LA newspaper on Owens River water acquisition, July 1905. "
            "Pro-aqueduct framing of what Owens Valley residents called theft."
        ),
    },

    # --- Tier 2: Women's Club Biographies ---
    # Applied uniformly across all biographies in this subfolder
    "__womens_club_default__": {
        "tier": 2,
        "bias_tag": "none",
        "bias_level": "none",
        "description": (
            "California Federation of Women's Clubs historical biography. "
            "Period accounts of influential California women."
        ),
    },
    
    # --- Tier 2: Owens Valley History Documents ---
    "__owensvalleyhistory_default__": {
        "tier": 2,
        "bias_tag": "none",
        "bias_level": "none",
        "description": (
            "Primary source document from owensvalleyhistory.com — "
            "local histories, period accounts, and newspaper archives "
            "of the Owens Valley region."
        ),
    }

    # --- Tier 3: Secondary and Reference Sources ---
    "california-geography-ch5-water.pdf": {
        "tier": 3,
        "bias_tag": "academic",
        "bias_level": "none",
        "description": (
            "Chapter 5 of California Geography by Jeremy Patrich. "
            "Water as a resource and conflict — academic secondary source."
        ),
    },
    "california-geography-ch12-great-basin.pdf": {
        "tier": 3,
        "bias_tag": "academic",
        "bias_level": "none",
        "description": (
            "Chapter 12 of California Geography by Jeremy Patrich. "
            "Great Basin geography — academic secondary source."
        ),
    },
    "story-of-inyo.pdf": {
        "tier": 3,
        "bias_tag": "settler_bias",
        "bias_level": "moderate",
        "description": (
            "Story of Inyo by W.A. Chalfant. Valuable local history but "
            "written from a settler perspective with racist views toward "
            "Native Americans. Use with critical caution."
        ),
    },
    "geology-and-water-resources-ov-report.pdf": {
        "tier": 3,
        "bias_tag": "institutional_bias",
        "bias_level": "mild",
        "description": (
            "USGS geology and water resources report on Owens Valley, "
            "produced in cooperation with the LA Department of Water and Power. "
            "Scientifically rigorous but carries institutional bias from LADWP involvement."
        ),
    },
}