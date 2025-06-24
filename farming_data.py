import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# In-memory database for farming information
# This would be replaced by a proper database in a production environment

# Farming techniques data
FARMING_TECHNIQUES = {
    "crops": [
        {
            "name": "Rice",
            "description": "A staple food crop grown in water-logged fields called paddies.",
            "growing_season": "Primarily during monsoon season (June to September)",
            "water_requirements": "High - requires flooded conditions for most varieties",
            "soil_requirements": "Clay soil with good water retention",
            "techniques": [
                "Puddle the soil before transplanting",
                "Maintain water level of 2-5 cm during growth phase",
                "Control weeds in early stages",
                "Apply balanced NPK fertilizers"
            ],
            "common_issues": [
                "Blast disease",
                "Brown plant hopper",
                "Stem borer",
                "Bacterial leaf blight"
            ]
        },
        {
            "name": "Wheat",
            "description": "One of the world's most important cereal crops used for bread, pasta, and other food products.",
            "growing_season": "Winter crop (October to April)",
            "water_requirements": "Moderate - sensitive to both drought and excess moisture",
            "soil_requirements": "Well-drained loamy soil with neutral pH",
            "techniques": [
                "Prepare a fine tilth seedbed",
                "Opt for timely sowing (Nov-Dec)",
                "First irrigation at crown root initiation stage",
                "Follow recommended spacing of 20-22.5 cm between rows"
            ],
            "common_issues": [
                "Rust diseases",
                "Powdery mildew",
                "Aphids",
                "Loose smut"
            ]
        },
        {
            "name": "Cotton",
            "description": "An important fiber crop grown for its lint which is used in textile production.",
            "growing_season": "Summer crop (April to November)",
            "water_requirements": "Moderate - sensitive to waterlogging",
            "soil_requirements": "Deep, well-drained black cotton soils or alluvial soils",
            "techniques": [
                "Use acid delinted seeds for better germination",
                "Maintain optimal plant population",
                "Implement integrated pest management",
                "Apply potassium for improving fiber quality"
            ],
            "common_issues": [
                "Bollworms",
                "Sucking pests (jassids, aphids, whitefly)",
                "Wilt disease",
                "Cotton leaf curl virus"
            ]
        },
        {
            "name": "Pulses (Lentils, Chickpeas, Pigeon Peas)",
            "description": "Leguminous crops that are rich sources of protein and improve soil fertility.",
            "growing_season": "Varies by type - both Rabi and Kharif seasons",
            "water_requirements": "Low to moderate - generally drought-resistant",
            "soil_requirements": "Well-drained loamy soil",
            "techniques": [
                "Inoculate seeds with Rhizobium culture",
                "Apply phosphatic fertilizers",
                "Control weeds in early stages",
                "Use trap crops for pest management"
            ],
            "common_issues": [
                "Pod borers",
                "Wilt",
                "Root rot",
                "Yellow mosaic virus"
            ]
        }
    ],
    "techniques": [
        {
            "name": "Organic Farming",
            "description": "A method of crop and livestock production that avoids the use of synthetic pesticides, fertilizers, growth regulators, and livestock feed additives.",
            "key_principles": [
                "Use of organic manures and biofertilizers",
                "Crop rotation and mixed cropping",
                "Biological pest control",
                "Green manuring"
            ],
            "benefits": [
                "Improved soil health and biodiversity",
                "Reduced pollution",
                "Potentially better nutritional quality",
                "Premium pricing for certified organic products"
            ],
            "challenges": [
                "Lower initial yields",
                "More labor-intensive",
                "Certification process can be complex",
                "Limited availability of organic inputs"
            ]
        },
        {
            "name": "Conservation Agriculture",
            "description": "Farming system that promotes minimum soil disturbance, permanent soil cover, and diversification of plant species.",
            "key_principles": [
                "Minimal or zero tillage",
                "Permanent soil cover (mulch or cover crops)",
                "Diverse crop rotations"
            ],
            "benefits": [
                "Reduced soil erosion",
                "Improved soil structure and health",
                "Lower production costs",
                "Better water infiltration and retention"
            ],
            "challenges": [
                "Initial investment in specialized equipment",
                "Knowledge-intensive",
                "Weed management can be challenging",
                "May require changes to traditional farming practices"
            ]
        },
        {
            "name": "Precision Farming",
            "description": "An approach where inputs are utilized in precise amounts to get increased average yields compared to traditional cultivation techniques.",
            "key_principles": [
                "GPS-guided operations",
                "Variable rate application of inputs",
                "Use of sensors and mapping technologies",
                "Data-driven decision making"
            ],
            "benefits": [
                "Optimized use of inputs",
                "Reduced environmental impact",
                "Higher productivity",
                "Lower costs in the long term"
            ],
            "challenges": [
                "High initial investment",
                "Requires technical knowledge",
                "Data management and interpretation",
                "May not be suitable for small holdings"
            ]
        },
        {
            "name": "Integrated Farming System",
            "description": "A mixed farming system that combines crop production with livestock, fishery, poultry, etc. to maximize farm productivity.",
            "key_principles": [
                "Efficient resource recycling",
                "Multiple income sources",
                "Reduced risk through diversification",
                "Closed nutrient cycles"
            ],
            "benefits": [
                "Year-round income generation",
                "Improved resource utilization",
                "Reduced vulnerability to market fluctuations",
                "Enhanced food security for the farm family"
            ],
            "challenges": [
                "Complex management",
                "Requires diverse skills",
                "Space constraints for small farmers",
                "Balancing resources among different components"
            ]
        }
    ],
    "soil_management": [
        {
            "name": "Soil Testing",
            "description": "Scientific analysis of soil samples to determine nutrient content, composition, and other characteristics.",
            "importance": "Helps in making informed decisions about soil amendments and fertilizer application.",
            "process": [
                "Collect soil samples from different parts of the field",
                "Mix samples to create a composite sample",
                "Send to a soil testing laboratory",
                "Interpret results and follow recommendations"
            ]
        },
        {
            "name": "Crop Rotation",
            "description": "Practice of growing different types of crops in the same area in sequenced seasons.",
            "benefits": [
                "Improves soil structure and fertility",
                "Helps in controlling pests and diseases",
                "Reduces soil erosion",
                "Manages soil nutrients efficiently"
            ],
            "examples": [
                "Cereals followed by legumes",
                "Deep-rooted crops followed by shallow-rooted ones",
                "Heavy feeders followed by light feeders"
            ]
        },
        {
            "name": "Green Manuring",
            "description": "Growing plants specifically for incorporating into the soil while green to improve soil fertility and structure.",
            "benefits": [
                "Adds organic matter to soil",
                "Improves soil structure",
                "Adds nitrogen (if leguminous plants are used)",
                "Suppresses weeds"
            ],
            "common_green_manure_crops": [
                "Sunhemp",
                "Dhaincha",
                "Cowpea",
                "Sesbania"
            ]
        }
    ]
}

# Government schemes data
GOVERNMENT_SCHEMES = [
    {
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "description": "A central sector scheme to provide income support to all landholding farmers' families in the country.",
        "benefits": "Rs. 6,000 per year transferred directly to farmers' bank accounts in three equal installments.",
        "eligibility": "All landholding farmers' families with cultivable land, subject to certain exclusions.",
        "how_to_apply": "Apply online through PM-KISAN portal or through Common Service Centers.",
        "documents_required": [
            "Aadhaar Card",
            "Land Records",
            "Bank Account Details"
        ]
    },
    {
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "description": "A crop insurance scheme that provides comprehensive risk coverage for crops against non-preventable natural risks.",
        "benefits": "Comprehensive risk insurance for pre-sowing to post-harvest losses due to natural calamities.",
        "eligibility": "All farmers, including sharecroppers and tenant farmers, growing notified crops.",
        "how_to_apply": "Through banks at the time of taking crop loans or directly through insurance companies.",
        "documents_required": [
            "Land Records/Tenant Agreement",
            "Bank Account Details",
            "Aadhaar Card",
            "Sowing Certificate"
        ]
    },
    {
        "name": "Kisan Credit Card (KCC)",
        "description": "A scheme that provides farmers with affordable credit for cultivation and other needs.",
        "benefits": [
            "Short-term loans for cultivation at subsidized interest rates",
            "Flexible repayment options",
            "Coverage for post-harvest expenses",
            "Insurance coverage for KCC holders"
        ],
        "eligibility": "All farmers, sharecroppers, tenant farmers, and SHGs of farmers.",
        "how_to_apply": "Apply at nearest bank branch or through online banking portals.",
        "documents_required": [
            "Land Records/Tenant Agreement",
            "Identity Proof",
            "Address Proof",
            "Passport Size Photographs"
        ]
    },
    {
        "name": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
        "description": "A scheme to ensure access to protective irrigation to all agricultural farms in the country.",
        "benefits": [
            "Improved water use efficiency",
            "Precision irrigation technologies",
            "Sustainable water conservation practices",
            "Enhanced crop productivity"
        ],
        "eligibility": "All farmers with focus on small and marginal farmers.",
        "how_to_apply": "Through State Agriculture/Irrigation Departments or their online portals.",
        "documents_required": [
            "Land Records",
            "Identity Proof",
            "Bank Account Details",
            "Water Source Details"
        ]
    },
    {
        "name": "National Mission for Sustainable Agriculture (NMSA)",
        "description": "A scheme to promote sustainable agriculture through climate change adaptation measures.",
        "benefits": [
            "Financial assistance for adopting sustainable agriculture practices",
            "Support for organic farming",
            "Soil health management",
            "Water conservation technologies"
        ],
        "eligibility": "All farmers with preference to small and marginal farmers.",
        "how_to_apply": "Through State Agriculture Departments or Krishi Vigyan Kendras.",
        "documents_required": [
            "Land Records",
            "Identity Proof",
            "Bank Account Details",
            "Project Proposal (if applicable)"
        ]
    }
]

# Farming laws and regulations data
FARMING_LAWS = [
    {
        "name": "Land Reforms Laws",
        "description": "Laws related to land ceiling, tenancy reforms, and distribution of agricultural land.",
        "key_provisions": [
            "Ceiling on land holdings",
            "Protection of tenants' rights",
            "Prohibition of leasing in some states",
            "Land consolidation provisions"
        ],
        "implications_for_farmers": "Affects land ownership, tenancy arrangements, and land transfers."
    },
    {
        "name": "Seed Laws",
        "description": "Laws governing the quality, production, and distribution of seeds.",
        "key_provisions": [
            "Seed certification requirements",
            "Quality standards for seeds",
            "Registration of seed varieties",
            "Penalties for selling substandard seeds"
        ],
        "implications_for_farmers": "Ensures access to quality seeds but may restrict use of farm-saved seeds in some cases."
    },
    {
        "name": "Pesticide Regulations",
        "description": "Laws governing the manufacture, sale, and use of pesticides in agriculture.",
        "key_provisions": [
            "Registration of pesticides",
            "Safety standards for pesticide use",
            "Licensing for pesticide dealers",
            "Ban on hazardous pesticides"
        ],
        "implications_for_farmers": "Ensures safety in pesticide use but requires compliance with usage guidelines."
    },
    {
        "name": "Water Laws",
        "description": "Laws related to irrigation water use, groundwater extraction, and water conservation.",
        "key_provisions": [
            "Regulation of groundwater extraction",
            "Water user associations",
            "Charges for irrigation water",
            "Rainwater harvesting mandates"
        ],
        "implications_for_farmers": "Affects access to water resources and costs for irrigation."
    },
    {
        "name": "Environmental Laws",
        "description": "Laws related to environmental protection that impact farming practices.",
        "key_provisions": [
            "Restrictions on stubble burning",
            "Regulations on chemical use near water bodies",
            "Protection of wetlands and forests",
            "Environmental impact assessment for large-scale farming"
        ],
        "implications_for_farmers": "May require changes in traditional farming practices to reduce environmental impact."
    }
]

def get_farming_techniques(category="all"):
    """
    Get information about farming techniques.
    
    Args:
        category (str): The category of farming techniques to retrieve (crops, techniques, soil_management, or all)
        
    Returns:
        dict: Information about farming techniques
    """
    try:
        if category == "all":
            return FARMING_TECHNIQUES
        elif category in FARMING_TECHNIQUES:
            return {category: FARMING_TECHNIQUES[category]}
        else:
            return {"error": f"Category '{category}' not found"}
    except Exception as e:
        logger.error(f"Error getting farming techniques: {e}")
        return {"error": "Failed to retrieve farming techniques"}

def get_government_schemes():
    """
    Get information about government schemes for farmers.
    
    Returns:
        list: List of government schemes
    """
    try:
        return GOVERNMENT_SCHEMES
    except Exception as e:
        logger.error(f"Error getting government schemes: {e}")
        return {"error": "Failed to retrieve government schemes"}

def get_farming_laws():
    """
    Get information about farming laws and regulations.
    
    Returns:
        list: List of farming laws and regulations
    """
    try:
        return FARMING_LAWS
    except Exception as e:
        logger.error(f"Error getting farming laws: {e}")
        return {"error": "Failed to retrieve farming laws"}

def search_farming_data(query):
    """
    Search for specific information across all farming data.
    
    Args:
        query (str): The search query
        
    Returns:
        dict: Search results
    """
    try:
        query = query.lower()
        results = {
            "techniques": [],
            "schemes": [],
            "laws": []
        }
        
        # Search in farming techniques
        for category in FARMING_TECHNIQUES:
            for item in FARMING_TECHNIQUES[category]:
                if query in json.dumps(item).lower():
                    results["techniques"].append(item)
        
        # Search in government schemes
        for scheme in GOVERNMENT_SCHEMES:
            if query in json.dumps(scheme).lower():
                results["schemes"].append(scheme)
        
        # Search in farming laws
        for law in FARMING_LAWS:
            if query in json.dumps(law).lower():
                results["laws"].append(law)
        
        return results
    except Exception as e:
        logger.error(f"Error searching farming data: {e}")
        return {"error": "Failed to search farming data"}
