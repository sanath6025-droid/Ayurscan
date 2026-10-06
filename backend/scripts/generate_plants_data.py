"""
Script to generate curated Ayurvedic plants dataset (backend/data/plants.json)
Contains 70 commonly recognized Ayurvedic plants with educational descriptions,
traditional uses, plant parts used, precautions, and warnings.
"""
import json
import os

PLANTS = [
    {
        "common_name": "Tulsi (Holy Basil)",
        "scientific_name": "Ocimum tenuiflorum",
        "ayurvedic_name": "Tulasi",
        "family": "Lamiaceae",
        "description": "An aromatic perennial shrub revered in traditional Indian medicine and household gardens. Noted for its distinct spicy-clove scent and purplish flowers.",
        "ayurvedic_uses": [
            "Traditionally used to balance Kapha and Vata doshas",
            "Considered an adaptogen (Rasayana) to support daily vitality and mental clarity",
            "Infused into decoctions (kashaya) for seasonal wellness and respiratory comfort"
        ],
        "traditional_uses": [
            "Brewed as herbal tea or tisane for everyday refreshment",
            "Kept in courtyards for natural air purification and cultural significance",
            "Fresh leaves crushed in poultices for minor external soothing"
        ],
        "plant_parts_used": ["Leaves", "Seeds", "Whole aerial parts"],
        "precautions": [
            "May possess mild blood-thinning and hypoglycemic properties",
            "Those scheduled for surgery should exercise caution",
            "Consult a healthcare professional during pregnancy or while breastfeeding"
        ],
        "warnings": [
            "Do not consume concentrated essential oils undiluted",
            "Not an alternative to medical attention for acute respiratory distress"
        ],
        "image_url": "https://images.unsplash.com/photo-1618164436241-4473940d1f5c?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=holy+basil+tulsi+ayurvedic+plant"
    },
    {
        "common_name": "Neem",
        "scientific_name": "Azadirachta indica",
        "ayurvedic_name": "Nimba",
        "family": "Meliaceae",
        "description": "A fast-growing evergreen tree native to the Indian subcontinent, famous for its bitter taste and cooling traditional attributes.",
        "ayurvedic_uses": [
            "Traditionally used to pacify Pitta and Kapha doshas",
            "Recognized as Tikta (bitter) and Shita (cooling) for blood purification rituals",
            "Used in classical formulations for supporting skin clarity and oral hygiene"
        ],
        "traditional_uses": [
            "Neem twigs traditionally chewed as natural toothbrushes (datun)",
            "Boiled leaf water used for soothing skin washes",
            "Dried leaves placed inside granaries and cupboards as a natural insect deterrent"
        ],
        "plant_parts_used": ["Leaves", "Bark", "Seeds", "Twigs", "Neem oil"],
        "precautions": [
            "Extremely bitter; excessive internal intake may cause gastric irritation",
            "Avoid internal consumption in infants, young children, and pregnant individuals",
            "May lower blood sugar levels when taken internally"
        ],
        "warnings": [
            "Neem seed oil should not be taken internally due to toxicity risks",
            "Seek medical guidance if taking oral anti-diabetic medications"
        ],
        "image_url": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=neem+tree+ayurveda+uses"
    },
    {
        "common_name": "Ashwagandha",
        "scientific_name": "Withania somnifera",
        "ayurvedic_name": "Ashvagandha",
        "family": "Solanaceae",
        "description": "A small woody shrub with yellow flowers and red berries, whose roots are widely celebrated in traditional systems as a premier rejuvenating tonic.",
        "ayurvedic_uses": [
            "Classified as a Balya (strength provider) and Rasayana (rejuvenator)",
            "Traditionally used to calm aggravated Vata and support sleep rhythm",
            "Included in ghee and milk decoctions to replenish Ojas (vital essence)"
        ],
        "traditional_uses": [
            "Root powder mixed with warm spiced milk and honey before rest",
            "Prepared as part of athletic and vitality lifestyle regimens",
            "Applied topically as a paste on tired joints"
        ],
        "plant_parts_used": ["Roots", "Leaves (rarely)"],
        "precautions": [
            "May cause drowsiness or interact with sedatives",
            "Individuals with thyroid conditions or autoimmune conditions should exercise discretion",
            "Not recommended during pregnancy without clinical oversight"
        ],
        "warnings": [
            "High doses may cause gastrointestinal discomfort or mild diarrhea",
            "Consult a licensed practitioner before combining with psychiatric prescriptions"
        ],
        "image_url": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=ashwagandha+plant+identification"
    },
    {
        "common_name": "Aloe Vera",
        "scientific_name": "Aloe vera",
        "ayurvedic_name": "Ghritakumari",
        "family": "Asphodelaceae",
        "description": "A succulent plant species with thick, fleshy leaves containing a clear soothing gel. Widely grown in household gardens and arid areas.",
        "ayurvedic_uses": [
            "Praised for its Sheeta (cooling) and Bhedana (gentle bowel movement) properties",
            "Traditionally used to soothe Pitta imbalances, particularly in the liver and skin",
            "Utilized in Kumari Asava, a classical fermented Ayurvedic preparation"
        ],
        "traditional_uses": [
            "Fresh inner fillet gel applied directly onto sunburned or dry skin",
            "Used in hair masks and scalp care preparations",
            "Inner pulp blended into fresh cooling morning tonics"
        ],
        "plant_parts_used": ["Inner leaf gel", "Leaf pulp", "Latex (traditional laxative, used with caution)"],
        "precautions": [
            "Yellow latex just beneath the rind is a strong stimulant laxative and can cause cramping",
            "Topical patch test recommended to check for contact dermatitis",
            "Avoid internal intake during pregnancy due to uterine stimulating risks"
        ],
        "warnings": [
            "Do not consume non-decolorized whole leaf extracts in large quantities",
            "Seek medical evaluation for serious burns or open wounds"
        ],
        "image_url": "https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=aloe+vera+plant+ayurveda"
    },
    {
        "common_name": "Turmeric",
        "scientific_name": "Curcuma longa",
        "ayurvedic_name": "Haridra",
        "family": "Zingiberaceae",
        "description": "A rhizomatous herbaceous perennial of the ginger family, celebrated for its brilliant golden color, warm aroma, and rich tradition.",
        "ayurvedic_uses": [
            "Traditionally considered Tridoshic, especially balancing for Kapha and Pitta",
            "Used to promote healthy digestion (Deepana) and metabolic clarity",
            "Applied in classical lepana (pastes) for promoting clear skin complexion"
        ],
        "traditional_uses": [
            "Foundational culinary spice in everyday cooking across Asia",
            "Brewed into 'Golden Milk' (haldi doodh) with warm milk and black pepper",
            "Used in traditional wedding ceremonies (Haldi ceremony) for ritual purification"
        ],
        "plant_parts_used": ["Rhizomes (fresh or dried powder)"],
        "precautions": [
            "May increase bile production; caution recommended for those with gallstones",
            "Large therapeutic doses may interact with blood thinners",
            "May stain skin, teeth, and fabrics bright yellow"
        ],
        "warnings": [
            "High supplemental doses of curcumin extracts should be discussed with a doctor",
            "Do not replace prescription anti-inflammatory therapy without professional guidance"
        ],
        "image_url": "https://images.unsplash.com/photo-1615485290176-32402ce12bb3?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=turmeric+plant+curcuma+longa"
    },
    {
        "common_name": "Ginger",
        "scientific_name": "Zingiber officinale",
        "ayurvedic_name": "Ardraka (fresh) / Shunthi (dry)",
        "family": "Zingiberaceae",
        "description": "A popular flowering plant whose rhizome is widely used as a pungent spice and traditional digestive remedy worldwide.",
        "ayurvedic_uses": [
            "Renowned as Vishwabhesaja ('universal medicine') in classical texts",
            "Known to kindle Agni (digestive fire) without severely provoking Pitta",
            "Traditionally taken with rock salt before meals to awaken taste and appetite"
        ],
        "traditional_uses": [
            "Fresh slices steeped in hot water with honey and lemon for seasonal warmth",
            "Crushed ginger added to curries, soups, and chai tea",
            "Warm ginger paste applied over tight neck or back muscles"
        ],
        "plant_parts_used": ["Fresh rhizome", "Dry rhizome powder"],
        "precautions": [
            "Large amounts may cause heartburn or mouth irritation in heat-sensitive individuals",
            "Use moderation if suffering from active peptic ulcers or severe acid reflux",
            "May mildly prolong bleeding time when consumed in heavy amounts"
        ],
        "warnings": [
            "Consult physician if taking anticoagulants or about to undergo surgery",
            "Do not use as sole intervention for severe dehydration or intractable vomiting"
        ],
        "image_url": "https://images.unsplash.com/photo-1615485500704-8e990f9900f7?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=ginger+zingiber+officinale+ayurveda"
    },
    {
        "common_name": "Amla (Indian Gooseberry)",
        "scientific_name": "Phyllanthus emblica",
        "ayurvedic_name": "Amalaki",
        "family": "Phyllanthaceae",
        "description": "A deciduous tree producing sour, fibrous green fruits known for exceptional nutrient density and natural vitamin C content.",
        "ayurvedic_uses": [
            "Foundational cornerstone of Triphala and the famed Chyawanprash formulation",
            "Possesses five of the six tastes (lacking only salty), balancing all three doshas",
            "Revered as a prime Rasayana for longevity, eye wellness, and hair health"
        ],
        "traditional_uses": [
            "Fresh fruit pickled, candied (murabba), or juiced",
            "Dried fruit powder applied with henna or coconut oil to hair roots",
            "Daily morning spoon of Amla powder with lukewarm water"
        ],
        "plant_parts_used": ["Fruit", "Seeds", "Leaves"],
        "precautions": [
            "High sourness may slightly chill the body if consumed late at night",
            "May lower blood glucose; monitor if taking anti-diabetic medications",
            "May increase tendency to bruise if taken in extreme doses"
        ],
        "warnings": [
            "Ensure clean source free of heavy metal contamination in commercial powders",
            "Not a cure-all substitute for balanced nutrition and clinical care"
        ],
        "image_url": "https://images.unsplash.com/photo-1546548970-71785318a17b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=amla+amalaki+phyllanthus+emblica"
    },
    {
        "common_name": "Brahmi (Water Hyssop)",
        "scientific_name": "Bacopa monnieri",
        "ayurvedic_name": "Brahmi",
        "family": "Plantaginaceae",
        "description": "A creeping, perennial succulent herb with small white flowers growing naturally in damp, marshy wetlands.",
        "ayurvedic_uses": [
            "Prime Medhya Rasayana (herbal intellect enhancer and mental tonic)",
            "Traditionally used to support memory retention, clarity, and restful focus",
            "Balancing to Pitta and Vata, especially calming overactive mental chatter"
        ],
        "traditional_uses": [
            "Brahmi leaves cooked lightly in traditional coastal Indian cuisines",
            "Infused in herbal ghee (Brahmi Ghrita) or hair oils for cooling the scalp",
            "Steeped as a gentle evening tea alongside gotu kola or chamomile"
        ],
        "plant_parts_used": ["Whole herb", "Leaves", "Stems"],
        "precautions": [
            "May cause mild stomach cramps or dry mouth when taken on an empty stomach",
            "May cause drowsiness or bradycardia (slow heart rate) at high doses",
            "Exercise caution when combining with cholinergic or thyroid drugs"
        ],
        "warnings": [
            "Due to marshy habitat, verify that harvesting sources are tested for heavy metals",
            "Do not discontinue neurological medications in favor of herbal supplements"
        ],
        "image_url": "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=bacopa+monnieri+brahmi+herb"
    },
    {
        "common_name": "Giloy (Heart-Leaved Moonseed)",
        "scientific_name": "Tinospora cordifolia",
        "ayurvedic_name": "Guduchi / Amrita",
        "family": "Menispermaceae",
        "description": "A vigorous climbing deciduous shrub with distinctive heart-shaped leaves and aerial roots, known traditionally as 'Amrita' (immortal nectar).",
        "ayurvedic_uses": [
            "Known as a renowned Jvarahara (traditional temperature balancer)",
            "Tridoshic herb that gently kindles digestion while calming Pitta heat",
            "Used to support resilience, vitality, and metabolic equilibrium"
        ],
        "traditional_uses": [
            "Fresh climbing stems boiled into bitter decoctions (Guduchi Kwath)",
            "Starch extracted as white sediment known as 'Guduchi Satva'",
            "Grown over Neem trees ('Neem Giloy') for enhanced traditional bitterness"
        ],
        "plant_parts_used": ["Mature stems", "Leaves", "Roots"],
        "precautions": [
            "May modulate blood sugar; monitor levels if on diabetic therapy",
            "Avoid excessive use in individuals with active autoimmune conditions",
            "Not established as safe for unsupervised use during pregnancy"
        ],
        "warnings": [
            "Must be distinguished correctly from other wild vine lookalikes",
            "Avoid unregulated heavy extracts with poor botanical authentication"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=tinospora+cordifolia+giloy+guduchi"
    },
    {
        "common_name": "Shatavari",
        "scientific_name": "Asparagus racemosus",
        "ayurvedic_name": "Shatavari",
        "family": "Asparagaceae",
        "description": "A woody climbing asparagus species with fine needle-like cladodes, fragrant white flowers, and tuberous root clusters.",
        "ayurvedic_uses": [
            "Celebrated as a prime female reproductive tonic and Rasayana",
            "Sweet and bitter in taste, with unctuous (Snigdha) and cooling (Shita) properties",
            "Balances Pitta and Vata, nourishing bodily tissues (Dhatus) and breast milk"
        ],
        "traditional_uses": [
            "Root powder taken with warm milk, ghee, and raw sugar",
            "Used across life transitions including postpartum and menopause",
            "Included in calming tonics for digestive acidity"
        ],
        "plant_parts_used": ["Tuberous roots"],
        "precautions": [
            "Being sweet and heavy, it may slightly increase Kapha dosha in excess",
            "Avoid in cases of severe fluid retention or kidney edema",
            "Individuals with estrogen-sensitive conditions should seek medical advice"
        ],
        "warnings": [
            "Persons allergic to asparagus family plants should avoid this species",
            "Not an alternative to medical treatment for infertility or endocrine disorders"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=asparagus+racemosus+shatavari"
    },
    {
        "common_name": "Hibiscus",
        "scientific_name": "Hibiscus rosa-sinensis",
        "ayurvedic_name": "Japa",
        "family": "Malvaceae",
        "description": "A bushy evergreen shrub featuring large, vivid red trumpet-shaped flowers with prominent staminal columns, widely cultivated in tropical gardens.",
        "ayurvedic_uses": [
            "Traditionally prized for cooling Pitta and purifying Rakta (blood)",
            "Extensively incorporated into classical Keshya (hair revitalizing) oils",
            "Petals used in decoctions to encourage natural balance during menstrual cycles"
        ],
        "traditional_uses": [
            "Crushed fresh petals and leaves blended into a natural mucilaginous shampoo",
            "Dried petals brewed into tangy, ruby-red herbal tisanes",
            "Offered traditionally in sacred rituals and festivities"
        ],
        "plant_parts_used": ["Flowers (petals)", "Leaves", "Roots"],
        "precautions": [
            "May possess mild emmenagogue properties; use moderation during pregnancy",
            "May modestly lower systemic blood pressure",
            "Hibiscus tea has high acidity that may affect sensitive tooth enamel"
        ],
        "warnings": [
            "Garden plants treated with synthetic pesticides should not be eaten or brewed",
            "Check for interactions with anti-hypertensive medications"
        ],
        "image_url": "https://images.unsplash.com/photo-1550950158-d0d960dff51b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=hibiscus+rosa+sinensis+ayurveda"
    },
    {
        "common_name": "Moringa (Drumstick Tree)",
        "scientific_name": "Moringa oleifera",
        "ayurvedic_name": "Shigru",
        "family": "Moringaceae",
        "description": "A fast-growing drought-resistant tree famous for hanging elongated seed pods and nutrient-packed bipinnate leaves.",
        "ayurvedic_uses": [
            "Recognized for its Tikshna (sharp) and Ushna (warming) qualities",
            "Traditionally used to clear Kapha and Vata accumulations",
            "Used to encourage joint comfort and natural metabolic vitality"
        ],
        "traditional_uses": [
            "Tender leaves sauteed as greens or simmered in sambar and dals",
            "Immature pods cooked in curries and soups for culinary richness",
            "Dried leaf powder added to smoothies and teas as a green superfood"
        ],
        "plant_parts_used": ["Leaves", "Seed pods (drumsticks)", "Seeds", "Bark", "Roots"],
        "precautions": [
            "Moringa bark and root contain alkaloids that can stimulate uterine contractions and must be avoided during pregnancy",
            "Leaves have mild laxative properties in unaccustomed stomachs",
            "May lower blood pressure and blood glucose"
        ],
        "warnings": [
            "Avoid root and bark extracts without specialized clinical direction",
            "Consult physician if taking thyroid hormone medication"
        ],
        "image_url": "https://images.unsplash.com/photo-1599818818559-9bc95a1a1f0c?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=moringa+oleifera+tree+identification"
    },
    {
        "common_name": "Curry Leaf",
        "scientific_name": "Murraya koenigii",
        "ayurvedic_name": "Kaidarya / Surabhinimba",
        "family": "Rutaceae",
        "description": "A small aromatic tree native to India and Sri Lanka, beloved for its distinctive fragrant foliage essential to South Asian cooking.",
        "ayurvedic_uses": [
            "Stimulates Agni (digestive fire) and relieves mild gastrointestinal sluggishness",
            "Historically regarded as beneficial for hair pigmentation and follicle strength",
            "Balances Kapha and Pitta doshas when used in moderate culinary quantities"
        ],
        "traditional_uses": [
            "Tempered in hot mustard oil or ghee as the foundation for curries and chutneys",
            "Leaves simmered in coconut oil to create fragrant traditional hair tonics",
            "Fresh leaf paste taken with buttermilk for morning digestive harmony"
        ],
        "plant_parts_used": ["Fresh leaves", "Bark", "Roots"],
        "precautions": [
            "Safe in culinary amounts; medicinal extracts should not be overused",
            "Wash leaves thoroughly to remove garden dust or agricultural sprays",
            "Avoid consuming raw berries"
        ],
        "warnings": [
            "The seeds are considered toxic and should not be consumed",
            "Do not confuse with the ornamental curry plant (Helichrysum italicum)"
        ],
        "image_url": "https://images.unsplash.com/photo-1618164435735-413d3b066c9a?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=curry+leaves+murraya+koenigii"
    },
    {
        "common_name": "Mint (Spearmint / Garden Mint)",
        "scientific_name": "Mentha spicata",
        "ayurvedic_name": "Pudina",
        "family": "Lamiaceae",
        "description": "A fast-spreading herbaceous perennial with bright green serrated leaves and a clean, refreshing aromatic fragrance.",
        "ayurvedic_uses": [
            "Mildly warming initially with a cooling post-digestive sensation",
            "Traditionally used to alleviate gas, bloating, and sluggish appetite",
            "Pacifies aggravated Pitta and Kapha, providing refreshing mental clarity"
        ],
        "traditional_uses": [
            "Essential ingredient in fresh coriander-mint chutneys and raitas",
            "Infused in hot or cold water for soothing digestive teas",
            "Crushed leaves inhaled for temporary relief of stuffy seasonal airways"
        ],
        "plant_parts_used": ["Leaves", "Aerial shoots"],
        "precautions": [
            "May relax the lower esophageal sphincter, exacerbating acid reflux in GERD patients",
            "Use with caution in those with gallbladder inflammation",
            "Avoid applying concentrated essential oils directly near the faces of young children"
        ],
        "warnings": [
            "Pure mint essential oil must not be ingested undiluted",
            "Consult a practitioner if suffering from severe chronic gastric symptoms"
        ],
        "image_url": "https://images.unsplash.com/photo-1608686207856-001b95cf60ca?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=mint+pudina+mentha+spicata"
    },
    {
        "common_name": "Lemongrass",
        "scientific_name": "Cymbopogon citratus",
        "ayurvedic_name": "Rohisha / Bhutrina",
        "family": "Poaceae",
        "description": "A tropical clumping grass with aromatic strap-like foliage that gives off a vibrant lemon-citrus fragrance when crushed.",
        "ayurvedic_uses": [
            "Traditionally used as a light (Laghu) digestive and diaphoretic herb",
            "Helps pacify Kapha and Vata, clearing heavy or sluggish sensations",
            "Used in herbal steams and teas during seasonal temperature shifts"
        ],
        "traditional_uses": [
            "Stems crushed and brewed into soothing herbal teas and soups",
            "Planted around verandas and porches as a natural mosquito deterrent",
            "Extracted essential oil used in aromatherapeutic diffusers and foot soaks"
        ],
        "plant_parts_used": ["Stalks", "Leaves", "Essential oil"],
        "precautions": [
            "May stimulate menstrual flow in large medicinal quantities; avoid high doses in pregnancy",
            "Direct application of essential oil can irritate sensitive skin; always dilute",
            "Drink plenty of water when using diaphoretic herbs"
        ],
        "warnings": [
            "Do not ingest concentrated lemongrass essential oil internally",
            "Do not substitute for immediate medical care in high persistent fevers"
        ],
        "image_url": "https://images.unsplash.com/photo-1514733670139-4d87a1941d55?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=cymbopogon+citratus+lemongrass"
    },
    {
        "common_name": "Fenugreek",
        "scientific_name": "Trigonella foenum-graecum",
        "ayurvedic_name": "Methi",
        "family": "Fabaceae",
        "description": "An annual legume producing trifoliate clover-like leaves and slender pods filled with golden-brown aromatic rhombic seeds.",
        "ayurvedic_uses": [
            "Classified as Ushna (warming) and Dipana (kindling digestive fire)",
            "Traditionally used to manage Vata and Kapha, especially for joints and digestion",
            "Noted in classical texts for supporting lactation (Stanyajanana)"
        ],
        "traditional_uses": [
            "Fresh green leaves (methi saag) cooked into rotis, curries, and vegetable sautés",
            "Seeds soaked overnight and water consumed in the morning for metabolic support",
            "Sprouted seeds eaten in salads for digestive fiber and bitter balance"
        ],
        "plant_parts_used": ["Seeds", "Fresh green leaves"],
        "precautions": [
            "High amounts of seeds can lower blood glucose and interact with insulin therapies",
            "May cause uterine contractions in large medicinal quantities; avoid excessive seeds during pregnancy",
            "Can impart a maple-syrup-like aroma to sweat and urine"
        ],
        "warnings": [
            "Individuals with peanut or chickpea allergies may experience cross-reactivity",
            "Do not use high therapeutic doses without monitoring blood sugar levels"
        ],
        "image_url": "https://images.unsplash.com/photo-1599940824399-b87987ceb72a?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=fenugreek+methi+trigonella"
    },
    {
        "common_name": "Ceylon Cinnamon",
        "scientific_name": "Cinnamomum verum",
        "ayurvedic_name": "Tvak",
        "family": "Lauraceae",
        "description": "An evergreen tree native to Sri Lanka and southern India, yielding delicate, thin-layered fragrant bark with a sweet-warm flavor.",
        "ayurvedic_uses": [
            "Warming in nature, balancing Vata and Kapha while supporting healthy circulation",
            "Part of the classical Trijataka and Chaturjata herbal spice combinations",
            "Encourages warmth in extremities and supports metabolic energy"
        ],
        "traditional_uses": [
            "Rolled quill bark ground into fine baking and dessert spice",
            "Steeped with whole cloves and cardamom into restorative chai tea",
            "Used in tooth powders for pleasant breath and gum tonicity"
        ],
        "plant_parts_used": ["Inner bark quills", "Leaves", "Cinnamon oil"],
        "precautions": [
            "Ceylon cinnamon (true cinnamon) has far lower coumarin levels than cassia, making it safer for frequent consumption",
            "Excessive doses can aggravate Pitta dosha causing burning sensation or heat flush",
            "Caution for individuals on anticoagulants or antidiabetic drugs"
        ],
        "warnings": [
            "Do not consume concentrated cinnamon essential oil internally",
            "Beware of mislabeled cassia bark which contains high hepatotoxic coumarin"
        ],
        "image_url": "https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=cinnamomum+verum+true+cinnamon"
    },
    {
        "common_name": "Black Pepper",
        "scientific_name": "Piper nigrum",
        "ayurvedic_name": "Maricha",
        "family": "Piperaceae",
        "description": "A perennial woody vine producing clusters of drupes that dry into pungent black peppercorns, famed as the 'king of spices'.",
        "ayurvedic_uses": [
            "One of the three components of the revered classical Trikatu formula",
            "Stimulates digestive fire (Deepana) and burns accumulated metabolic toxins (Ama)",
            "Assists in clearing respiratory mucus caused by Kapha congestion"
        ],
        "traditional_uses": [
            "Universal culinary seasoning across virtually all world cultures",
            "Crushed with honey as a traditional home remedy for seasonal throat scratchiness",
            "Used to enhance bioavailability of herbs such as turmeric (via piperine)"
        ],
        "plant_parts_used": ["Dried unripe fruits (peppercorns)"],
        "precautions": [
            "Pungent and heating; can irritate stomach lining in active gastritis or ulcers",
            "Increases intestinal absorption of numerous pharmaceuticals, potentially altering drug levels",
            "Avoid breathing in fine dust to prevent sneezing and nasal irritation"
        ],
        "warnings": [
            "Exercise care when taking prescription medications metabolized by CYP450 enzymes",
            "Do not apply whole crushed pepper near open cuts or delicate mucous membranes"
        ],
        "image_url": "https://images.unsplash.com/photo-1508746829417-e6f548d8d6ed?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=piper+nigrum+black+pepper+ayurveda"
    },
    {
        "common_name": "Green Cardamom",
        "scientific_name": "Elettaria cardamomum",
        "ayurvedic_name": "Ela",
        "family": "Zingiberaceae",
        "description": "A perennial reed-like herb native to the southern Indian rainforests, producing triangular papery pods with aromatic black seeds.",
        "ayurvedic_uses": [
            "Slightly cooling compared to other spices, gentle on Pitta while balancing Vata and Kapha",
            "Traditionally chewed post-meals to refresh breath (Mukhadoshahara) and aid digestion",
            "Included in formulations to soothe nausea and support respiratory smoothness"
        ],
        "traditional_uses": [
            "Crushed pods steeped in traditional teas, rice puddings (kheer), and biryanis",
            "Pods chewed as a post-prandial mouth freshener",
            "Infused into warm desserts to temper the heavy qualities of milk and sugar"
        ],
        "plant_parts_used": ["Seed pods", "Seeds"],
        "precautions": [
            "Generally very safe in culinary and herbal tea amounts",
            "Large therapeutic quantities may trigger gallbladder discomfort in gallstone sufferers",
            "Keep pods whole until use to preserve delicate volatile oils"
        ],
        "warnings": [
            "Avoid ingestion of concentrated cardamom oils without expert guidance",
            "Not a substitute for emergency intervention in acute gastrointestinal colic"
        ],
        "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=elettaria+cardamomum+green+cardamom"
    },
    {
        "common_name": "Clove",
        "scientific_name": "Syzygium aromaticum",
        "ayurvedic_name": "Lavanga",
        "family": "Myrtaceae",
        "description": "An aromatic medium-sized evergreen tree whose unopened flower buds are harvested and dried into nail-shaped fragrant spice cloves.",
        "ayurvedic_uses": [
            "Deeply aromatic and warming, classified as Kaphapittahara (in balance)",
            "Traditionally used for oral clarity, soothing gums, and breath refinement",
            "Kindles digestive fire and eases cold, sluggish abdominal distension"
        ],
        "traditional_uses": [
            "Whole cloves held near an aching tooth for soothing comfort",
            "Key component of chai masala, garam masala, and mulled infusions",
            "Boiled with ginger and cinnamon for seasonal chest warming decoctions"
        ],
        "plant_parts_used": ["Dried flower buds", "Clove oil"],
        "precautions": [
            "Clove oil contains eugenol, which is very potent and can cause tissue irritation or burns if undiluted",
            "May inhibit platelet aggregation; stop medicinal intake prior to surgery",
            "Avoid giving pure clove oil to infants and small children"
        ],
        "warnings": [
            "Never swallow pure clove essential oil undiluted",
            "Do not substitute clove oil for professional dental care in severe infections"
        ],
        "image_url": "https://images.unsplash.com/photo-1601039641847-7857b994d704?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=syzygium+aromaticum+clove+lavanga"
    },
    {
        "common_name": "Gotu Kola",
        "scientific_name": "Centella asiatica",
        "ayurvedic_name": "Mandukaparni",
        "family": "Apiaceae",
        "description": "A low-growing creeping herb with kidney-shaped leaves found throughout tropical and subtropical wetlands.",
        "ayurvedic_uses": [
            "Renowned Medhya Rasayana for fostering mental alertness and calm awareness",
            "Cooling to Pitta, soothing heated conditions and supporting healthy skin tissue",
            "Used to tonify connective tissue, veins, and nervous system vitality"
        ],
        "traditional_uses": [
            "Fresh leaves eaten in traditional Sri Lankan pennywort salads (sambol)",
            "Steeped as a gentle brain tonic tea for students and meditators",
            "Applied in herbal poultices to support smooth scar and skin healing"
        ],
        "plant_parts_used": ["Whole herb", "Leaves"],
        "precautions": [
            "Can cause mild headache or dizziness in exceptionally high doses",
            "May interact with sedatives and liver medications",
            "Avoid excessive use during pregnancy"
        ],
        "warnings": [
            "Ensure harvesting from unpolluted water sources to avoid heavy metals",
            "Do not confuse with Bacopa monnieri though both share Medhya uses"
        ],
        "image_url": "https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=centella+asiatica+gotu+kola"
    },
    {
        "common_name": "Shankhpushpi",
        "scientific_name": "Convolvulus prostratus",
        "ayurvedic_name": "Shankhapushpi",
        "family": "Convolvulaceae",
        "description": "A prostrate, hairy perennial herb with conch-shell-like pale blue or white blossoms flourishing in sandy plains.",
        "ayurvedic_uses": [
            "Celebrated classical Medhya herb specifically beneficial for nervous composure",
            "Known for its Medhya (intellect-promoting) and Nidrajanana (sleep supporting) virtues",
            "Balances all three doshas, especially calming agitated Pitta and Vata"
        ],
        "traditional_uses": [
            "Whole herb syrup administered to students during examination periods",
            "Consumed with milk and raw honey before bedtime for peaceful sleep",
            "Included in calming morning herbal teas"
        ],
        "plant_parts_used": ["Whole plant (Panchanga)"],
        "precautions": [
            "May cause mild sedation and lower blood pressure",
            "Caution when combining with anti-epileptic or sedative medications",
            "Safety during pregnancy and lactation has not been clinically determined"
        ],
        "warnings": [
            "Do not stop anti-seizure medication without consulting a neurologist",
            "Ensure authentication of botanical identity as related species are sometimes substituted"
        ],
        "image_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=shankhpushpi+plant+ayurveda"
    },
    {
        "common_name": "Haritaki (Chebulic Myrobalan)",
        "scientific_name": "Terminalia chebula",
        "ayurvedic_name": "Haritaki",
        "family": "Combretaceae",
        "description": "A grand deciduous tree producing ribbed drupe fruits, traditionally hailed as the 'Mother of Herbs' in Tibetan and Ayurvedic traditions.",
        "ayurvedic_uses": [
            "Cornerstone member of the fundamental Triphala formulation",
            "Has five tastes (all except salty); predominantly astringent and sweet post-digestive",
            "Acts as a gentle bowel regulator (Anulomana) and metabolic detoxifier"
        ],
        "traditional_uses": [
            "Taken at bedtime with warm water for natural digestive regulation",
            "Consolidated with different seasonal adjuvants (Ritu Haritaki) for yearly vitality",
            "Used as a mouth gargle for gum strength and oral health"
        ],
        "plant_parts_used": ["Dried fruit rind"],
        "precautions": [
            "Strongly astringent; may aggravate dryness or acute exhaustion if taken improperly",
            "Avoid in cases of severe acute diarrhea, dehydration, or emaciation",
            "Not recommended during pregnancy due to downward-moving energetic actions"
        ],
        "warnings": [
            "Consult a practitioner before using as a daily long-term single herb",
            "Do not use as a substitute for medical evaluation of persistent rectal bleeding"
        ],
        "image_url": "https://images.unsplash.com/photo-1546548970-71785318a17b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=terminalia+chebula+haritaki"
    },
    {
        "common_name": "Bibhitaki (Belleric Myrobalan)",
        "scientific_name": "Terminalia bellirica",
        "ayurvedic_name": "Bibhitaka",
        "family": "Combretaceae",
        "description": "A tall forest canopy tree producing grey, velvety globular fruits with high tannin content.",
        "ayurvedic_uses": [
            "Third pillar of the revered Triphala triad",
            "Traditionally indicated for purifying Kapha imbalances in lungs and throat",
            "Supports clear voice, respiratory comfort, and balanced intestinal mucosa"
        ],
        "traditional_uses": [
            "Fruit pulp roasted and mixed with rock sugar for soothing dry throat tickles",
            "Infused in traditional eye washes and scalp rinse formulations",
            "Blended with Haritaki and Amalaki into Triphala powder"
        ],
        "plant_parts_used": ["Dried fruit rind"],
        "precautions": [
            "High tannin content may cause temporary astringent dryness in mouth and stomach",
            "Take with plenty of warm water",
            "Avoid large therapeutic doses during pregnancy"
        ],
        "warnings": [
            "The inner seed kernels are reported to possess narcotic properties; use fruit rind only",
            "Seek medical guidance for persistent productive coughs or chest symptoms"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=terminalia+bellirica+bibhitaki"
    },
    {
        "common_name": "Arjuna",
        "scientific_name": "Terminalia arjuna",
        "ayurvedic_name": "Arjuna",
        "family": "Combretaceae",
        "description": "A majestic riverine tree with smooth, mottled pinkish-grey buttressed trunk that naturally sheds its thick outer bark.",
        "ayurvedic_uses": [
            "Foremost classical Hridya (cardiac tonic) in traditional Ayurvedic literature",
            "Possesses Kashaya (astringent) taste and cooling potency, pacifying Pitta and Kapha",
            "Traditionally simmered in milk (Arjuna Ksheerapaka) to support cardiac tissue tone"
        ],
        "traditional_uses": [
            "Bark decoctions taken daily for emotional and cardiovascular centered wellness",
            "Used topically in washes for wound astringency and firming tissues",
            "Combined with spices to moderate its earthy, drying taste"
        ],
        "plant_parts_used": ["Stem bark"],
        "precautions": [
            "May lower blood pressure and pulse rate mildly",
            "Can interact with cardiac medications, beta blockers, and diuretics",
            "Do not consume without clinical guidance if diagnosed with heart disease"
        ],
        "warnings": [
            "Arjuna is not a replacement for medical emergency treatment for chest pain or myocardial infarction",
            "Always consult a cardiologist before taking herbal heart tonics"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=terminalia+arjuna+tree+ayurveda"
    },
    {
        "common_name": "Punarnava (Spreading Hogweed)",
        "scientific_name": "Boerhavia diffusa",
        "ayurvedic_name": "Punarnava",
        "family": "Nyctaginaceae",
        "description": "A diffuse prostrate perennial weed with pink-purple flowers whose name translates to 'that which renews or restores'.",
        "ayurvedic_uses": [
            "Hailed for Shothahara (fluid balance and swelling reduction) properties",
            "Traditionally used to rejuvenate the kidneys, urinary tract, and liver function",
            "Balances all three doshas, particularly useful for clearing excess Kapha water"
        ],
        "traditional_uses": [
            "Tender leaves cooked as seasonal greens in rural culinary dishes",
            "Root decoctions brewed for easing heaviness in the lower limbs",
            "Included in classical formulations like Punarnavasava"
        ],
        "plant_parts_used": ["Roots", "Whole herb"],
        "precautions": [
            "Acts as a mild natural diuretic; monitor electrolyte balance with prolonged use",
            "May interact with prescription diuretic and hypertension medications",
            "Not recommended during pregnancy without clinical supervision"
        ],
        "warnings": [
            "Do not use in place of medical treatment for kidney failure or congestive heart failure",
            "Seek emergency care for sudden severe swelling or reduced urine output"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=boerhavia+diffusa+punarnava"
    },
    {
        "common_name": "Guggulu (Indian Bdellium)",
        "scientific_name": "Commiphora mukul",
        "ayurvedic_name": "Guggulu",
        "family": "Burseraceae",
        "description": "A spiny, stunted shrub native to arid regions of northwestern India, producing a fragrant oleo-gum-resin.",
        "ayurvedic_uses": [
            "Celebrated for Medohara (lipid and tissue balancing) and Sandhivata (joint comfort) actions",
            "A powerful Yogavahi (carrier herb) that enhances other herbal compounds",
            "Used extensively in compound tablets such as Yogaraj Guggulu and Triphala Guggulu"
        ],
        "traditional_uses": [
            "Purified resin rolled into classical pill formulations",
            "Incense made from raw resin used in traditional cleansing rituals",
            "Applied in warm joint pastes for deep tissue soothing"
        ],
        "plant_parts_used": ["Purified oleo-gum-resin (Niryasa)"],
        "precautions": [
            "Must undergo traditional purification (Shodhana) before medicinal use",
            "May stimulate thyroid function and affect lipid levels",
            "Can cause skin rashes, diarrhea, or interact with blood thinners and contraceptives"
        ],
        "warnings": [
            "Strictly contraindicated during pregnancy due to uterine stimulating actions",
            "Unpurified resin can cause severe gastric irritation and kidney strain"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=commiphora+mukul+guggul"
    },
    {
        "common_name": "Manjistha (Indian Madder)",
        "scientific_name": "Rubia cordifolia",
        "ayurvedic_name": "Manjistha",
        "family": "Rubiaceae",
        "description": "A prickly climbing herb with whorled leaves and long cylindrical roots that yield an intense crimson dye.",
        "ayurvedic_uses": [
            "Renowned as a premier Rakta Shodhaka (blood purifier) and lymphatic detoxifier",
            "Possesses sweet, bitter, and astringent tastes with a cooling potency",
            "Traditionally used to soothe inflammatory Pitta conditions affecting the skin"
        ],
        "traditional_uses": [
            "Root powder blended with honey or clay for radiant facial masks",
            "Used historically as a natural organic red textile dye",
            "Decoctions consumed for balancing seasonal skin flare-ups"
        ],
        "plant_parts_used": ["Roots", "Stems"],
        "precautions": [
            "May temporarily tint urine and perspiration reddish-orange (harmless)",
            "Strongly astringent; may slightly aggravate Vata dryness if taken without moistening herbs",
            "Avoid during pregnancy and breastfeeding"
        ],
        "warnings": [
            "Ensure root source is authenticated and tested for contaminants",
            "Consult physician if managing chronic liver or kidney disease"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=rubia+cordifolia+manjistha"
    },
    {
        "common_name": "Bala (Country Mallow)",
        "scientific_name": "Sida cordifolia",
        "ayurvedic_name": "Bala",
        "family": "Malvaceae",
        "description": "A small hairy perennial shrub with small yellow blossoms, whose name literally translates to 'strength'.",
        "ayurvedic_uses": [
            "Renowned as Balya (strength provider) and Brimhana (nourishing)",
            "Pacifies aggravated Vata and Pitta, supporting muscle tone and nerve resilience",
            "Formulated into nourishing massage oils like Mahanarayan and Ksheerabala"
        ],
        "traditional_uses": [
            "Decocted in milk and sesame oil for neuromuscular massage therapy",
            "Roots stewed in vitality broths for convalescent recovery",
            "Ground into poultices for joint comfort"
        ],
        "plant_parts_used": ["Roots", "Leaves", "Seeds"],
        "precautions": [
            "Contains naturally occurring trace ephedrine alkaloids in seeds and aerial parts",
            "Can elevate heart rate and blood pressure if used in concentrated internal extracts",
            "Individuals with hypertension, glaucoma, or heart conditions must avoid internal use"
        ],
        "warnings": [
            "Do not consume unregulated ephedrine-containing supplements",
            "External oil massage is widely practiced and generally considered far gentler"
        ],
        "image_url": "https://images.unsplash.com/photo-1490750967868-88aa4486c946?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=sida+cordifolia+bala+plant"
    },
    {
        "common_name": "Licorice (Mulethi)",
        "scientific_name": "Glycyrrhiza glabra",
        "ayurvedic_name": "Yashtimadhu",
        "family": "Fabaceae",
        "description": "A herbaceous perennial legume producing sweet fibrous subterranean stolons, widely recognized in ancient pharmacology.",
        "ayurvedic_uses": [
            "Possesses intense natural sweetness (Madhura), cooling potency, and soothing unctuousness",
            "Pacifies Pitta and Vata, soothing the stomach lining and vocal cords (Kanthya)",
            "Harmonizes and softens harsh formulas while providing adaptogenic resilience"
        ],
        "traditional_uses": [
            "Small root sticks chewed to soothe a hoarse voice or singers' throat",
            "Root powder simmered in warm milk or herbal teas for acid relief",
            "Blended into natural skincare pastes to brighten hyperpigmentation"
        ],
        "plant_parts_used": ["Peeled or unpeeled roots and stolons"],
        "precautions": [
            "Contains glycyrrhizin, which in large prolonged doses can cause sodium retention, potassium loss, and hypertension",
            "Limit high daily intake to no more than 4–6 consecutive weeks",
            "Contraindicated in severe hypertension, kidney failure, and congestive heart disease"
        ],
        "warnings": [
            "Pregnant women should avoid high medicinal consumption",
            "Consult a clinician if taking antihypertensives, corticosteroids, or cardiac glycosides"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=glycyrrhiza+glabra+yashtimadhu+licorice"
    },
    {
        "common_name": "Kalmegh (Green Chiretta / King of Bitters)",
        "scientific_name": "Andrographis paniculata",
        "ayurvedic_name": "Kalmegha / Bhunimba",
        "family": "Acanthaceae",
        "description": "An erect annual herb featuring dark green lance-shaped leaves and pink-spotted blossoms, famous for intense, piercing bitterness.",
        "ayurvedic_uses": [
            "Regarded as the 'King of Bitters' (Tikta Rasa) and profoundly cooling",
            "Historically utilized for liver support (Yakrit Utthejaka) and deep Pitta heat clearance",
            "Used in seasonal changes to support immunity and balance digestive agni"
        ],
        "traditional_uses": [
            "Leaves dried and steeped into extremely bitter herbal teas for seasonal sniffles",
            "Fresh leaf paste taken with honey to offset extreme bitterness",
            "Key ingredient in traditional polyherbal household tonics"
        ],
        "plant_parts_used": ["Whole aerial herb", "Leaves"],
        "precautions": [
            "Intense bitterness may cause mild stomach upset or nausea in high doses",
            "May possess antifertility and abortifacient actions; avoid in pregnancy and those trying to conceive",
            "Can interact with anticoagulants and anti-hypertensive drugs"
        ],
        "warnings": [
            "Do not exceed recommended herbal doses due to potential gastric distress",
            "Consult a physician for persistent high fevers or jaundice symptoms"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=andrographis+paniculata+kalmegh"
    },
    {
        "common_name": "Bhringraj (False Daisy)",
        "scientific_name": "Eclipta prostrata",
        "ayurvedic_name": "Bhringaraja",
        "family": "Asteraceae",
        "description": "A small branched annual herb with opposite leaves and dainty daisy-like white florets, thriving near moist fields and streams.",
        "ayurvedic_uses": [
            "Celebrated as the foremost Keshya (hair nourishing) herb in Ayurveda",
            "Known as a Rasayana that calms Pitta and supports liver health",
            "Supports restful sleep and soothing cranial massage when infused in oil"
        ],
        "traditional_uses": [
            "Fresh juice cooked into sesame or coconut oil for blackening and conditioning hair",
            "Leaf paste applied to the scalp for cooling mental fatigue",
            "Juice mixed with honey in modest doses for traditional liver tonics"
        ],
        "plant_parts_used": ["Whole plant", "Leaves", "Roots"],
        "precautions": [
            "Can cause mild chilling sensations if used as cold scalp oil in winter",
            "May cause loose stools if consumed in large raw quantities",
            "Patch test recommended prior to intensive scalp applications"
        ],
        "warnings": [
            "Avoid unregulated heavy extracts without authentic botanical validation",
            "Seek medical assessment for unexplained sudden hair shedding or scalp lesions"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=eclipta+prostrata+bhringraj"
    },
    {
        "common_name": "Kutki",
        "scientific_name": "Picrorhiza kurroa",
        "ayurvedic_name": "Katuki",
        "family": "Plantaginaceae",
        "description": "A delicate, threatened perennial Himalayan alpine herb with creeping rhizomes, prized for its potent hepatoprotective qualities.",
        "ayurvedic_uses": [
            "Profoundly bitter and cooling, pacifying excess Pitta and Kapha",
            "Traditionally used to stimulate healthy bile flow (Bhedana) and support liver function",
            "Used in classical formulations for clearing deep seasonal heat"
        ],
        "traditional_uses": [
            "Small pinch of root powder taken with honey before meals",
            "Formulated into Arogyavardhini Vati, a classic Ayurvedic compound",
            "Traditional tea for convalescent digestive revival"
        ],
        "plant_parts_used": ["Dried rhizome and roots"],
        "precautions": [
            "Pungent bitter taste with gentle purgative effects at higher doses",
            "Avoid in chronic diarrhea or severe Vata depletion",
            "Species is endangered; procure only from certified sustainable cultivation"
        ],
        "warnings": [
            "Never consume unauthenticated wild substitutes",
            "Seek medical care immediately for symptoms of acute jaundice or hepatitis"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=picrorhiza+kurroa+kutki"
    },
    {
        "common_name": "Vidarikand (Indian Kudzu)",
        "scientific_name": "Pueraria tuberosa",
        "ayurvedic_name": "Vidari",
        "family": "Fabaceae",
        "description": "A massive woody climber with huge underground tuberous storage roots, bearing purple-blue pea-like flowers.",
        "ayurvedic_uses": [
            "A prominent Rasayana and Brimhana (nourishing and tissue-building) herb",
            "Sweet in taste and cooling in potency, soothing Vata and Pitta",
            "Traditionally used to support lactation, vitality, and muscle endurance"
        ],
        "traditional_uses": [
            "Tuber powder simmered with whole milk, ghee, and dates for energy shakes",
            "Traditional convalescent food for weakness and rejuvenation",
            "Formulated into postpartum restorative confectionery"
        ],
        "plant_parts_used": ["Underground tubers"],
        "precautions": [
            "Heavy and sweet; can increase Kapha and mucus if overconsumed without digestive spices",
            "Caution for individuals with estrogen-sensitive conditions due to isoflavones",
            "Avoid in sluggish metabolism or obesity without active lifestyle"
        ],
        "warnings": [
            "Consult a physician if being treated for hormonal cancers",
            "Not an alternative to medical treatment for severe malnutrition"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=pueraria+tuberosa+vidarikand"
    },
    {
        "common_name": "Sarpagandha (Indian Snakeroot)",
        "scientific_name": "Rauvolfia serpentina",
        "ayurvedic_name": "Sarpagandha",
        "family": "Apocynaceae",
        "description": "An evergreen shrub with whorled leaves and red-to-black berries, historically famous as the source of reserpine.",
        "ayurvedic_uses": [
            "Possesses bitter taste and penetrating properties, traditionally used to pacify Vata and Kapha",
            "Historically utilized for high mental agitation, frenzy (Unmada), and restful sleep",
            "Recognized classical herb for cooling internal tension and circulatory stress"
        ],
        "traditional_uses": [
            "Traditionally administered in minute calibrated doses under expert Vaidya supervision",
            "Root paste historically applied to insect stings and reptile bites in folklore",
            "Used in classical mental calming pills (Sarpagandha Ghan Vati)"
        ],
        "plant_parts_used": ["Roots"],
        "precautions": [
            "Contains potent alkaloids (including reserpine) with pronounced hypotensive and sedative effects",
            "Strictly contraindicated in depression, active peptic ulcer, Parkinson's disease, and pregnancy",
            "Can cause significant nasal congestion, bradycardia, and lethargy"
        ],
        "warnings": [
            "Potent prescription-grade botanical; NEVER consume recreationally or without medical supervision",
            "Can cause dangerous interactions with psychiatric drugs, antidepressants, and anesthesia"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=rauvolfia+serpentina+sarpagandha"
    },
    {
        "common_name": "Vasaka (Malabar Nut)",
        "scientific_name": "Justicia adhatoda",
        "ayurvedic_name": "Vasa",
        "family": "Acanthaceae",
        "description": "A dense evergreen shrub with large lanceolate leaves and white tubular two-lipped flowers resembling a lion's mouth.",
        "ayurvedic_uses": [
            "Premier classical botanical for respiratory balance (Kasahara and Shvasahara)",
            "Bitter and astringent in taste with cooling potency, balancing Kapha and Pitta",
            "Supports clear bronchial airways, soothing throat irritation, and liquefying phlegm"
        ],
        "traditional_uses": [
            "Fresh leaf juice mixed with honey for seasonal coughs and throat comfort",
            "Leaves dried and brewed into warming chest syrups and decoctions (Vasa Avaleha)",
            "Applied in gentle herbal compresses for localized warmth"
        ],
        "plant_parts_used": ["Leaves", "Flowers", "Roots"],
        "precautions": [
            "Contains vasicine, an alkaloid that can stimulate uterine contractions; contraindicated during pregnancy",
            "High doses may cause vomiting, diarrhea, or nausea",
            "Use with caution in young children"
        ],
        "warnings": [
            "Strictly avoid during pregnancy due to abortifacient potential",
            "Seek immediate medical attention for hemoptysis (coughing blood) or acute shortness of breath"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=justicia+adhatoda+vasaka"
    },
    {
        "common_name": "Ajwain (Carom Seeds / Bishop's Weed)",
        "scientific_name": "Trachyspermum ammi",
        "ayurvedic_name": "Yavani",
        "family": "Apiaceae",
        "description": "An annual herbaceous plant producing small, oval striped seeds with a pungent thyme-like aroma due to high thymol content.",
        "ayurvedic_uses": [
            "Hot, sharp, and intensely aromatic; instantly pacifies Vata and Kapha in the gut",
            "Acts as a powerful carminative (Deepana, Pachana, and Shulahara)",
            "Quickly eases flatulence, abdominal bloating, and feeling of heaviness after rich meals"
        ],
        "traditional_uses": [
            "Pinch of seeds chewed with black salt and warm water after heavy dinners",
            "Roasted seeds tossed into dough for puris, samosas, and parathas to ease digestion",
            "Warmed in a cloth potli and applied over chest or stomach for soothing warmth"
        ],
        "plant_parts_used": ["Dried seeds (fruits)"],
        "precautions": [
            "Intensely heating (Ushna); can aggravate Pitta dosha if taken excessively, causing acidity or burning",
            "Use moderation during pregnancy; avoid high medicinal doses",
            "May irritate delicate oral mucosa if chewed in large handfuls"
        ],
        "warnings": [
            "Do not consume concentrated ajwain essential oil internally",
            "Not a cure for acute appendicitis or surgical abdominal emergencies"
        ],
        "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=trachyspermum+ammi+ajwain"
    },
    {
        "common_name": "Fennel",
        "scientific_name": "Foeniculum vulgare",
        "ayurvedic_name": "Mishreya / Shatapushpa",
        "family": "Apiaceae",
        "description": "A hardy perennial herb with feathery green foliage, golden umbel blooms, and sweet anise-flavored ribbed seeds.",
        "ayurvedic_uses": [
            "Gentle and balancing for all three doshas, especially calming Pitta without dampening Agni",
            "Kindles digestive capability while soothing spasms and burning sensations",
            "Traditionally given to nursing mothers to support gentle infant digestion"
        ],
        "traditional_uses": [
            "Chewed alongside sugar candy (mishri) at the conclusion of Indian restaurant meals",
            "Steeped into gentle calming tea for infant colic or sensitive stomachs",
            "Added to spice rubs and herbal mouth rinses for long-lasting freshness"
        ],
        "plant_parts_used": ["Seeds", "Foliage", "Bulb"],
        "precautions": [
            "Very safe in dietary amounts",
            "High concentrated therapeutic extracts may have mild estrogenic effects; avoid high doses in hormone-sensitive states",
            "May cause photosensitivity in rare sensitive individuals"
        ],
        "warnings": [
            "Avoid pure fennel essential oil in pregnant women and infants",
            "Consult pediatrician before administering herbal concoctions to newborn babies"
        ],
        "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=foeniculum+vulgare+fennel+saunf"
    },
    {
        "common_name": "Coriander",
        "scientific_name": "Coriandrum sativum",
        "ayurvedic_name": "Dhanyaka",
        "family": "Apiaceae",
        "description": "A widely cultivated annual herb whose fresh leaves are known as cilantro and whose dried aromatic spherical fruits serve as coriander seeds.",
        "ayurvedic_uses": [
            "Famous for its cooling (Shita) potency and gentle digestive kindling (Deepana)",
            "Traditionally used to clear urinary heat, burning micturition, and excess Pitta",
            "Used in classical cold infusions (Hima) for seasonal hydration and cooling"
        ],
        "traditional_uses": [
            "Seeds crushed into curry powders and spice pastes worldwide",
            "Overnight cold seed water consumed in the morning for soothing internal heat",
            "Fresh leaves chopped into fresh salsas, chutneys, and garnishes"
        ],
        "plant_parts_used": ["Seeds (fruits)", "Fresh leaves"],
        "precautions": [
            "Safe and nourishing as a culinary staple",
            "Mild diuretic action; stay hydrated",
            "Rare contact allergies may occur in sensitive individuals handling fresh foliage"
        ],
        "warnings": [
            "Seek medical testing for recurring or painful urinary tract infections",
            "Do not rely solely on seed infusions for clinical kidney conditions"
        ],
        "image_url": "https://images.unsplash.com/photo-1618164435735-413d3b066c9a?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=coriandrum+sativum+coriander+dhanya"
    },
    {
        "common_name": "Cumin",
        "scientific_name": "Cuminum cyminum",
        "ayurvedic_name": "Jeeraka",
        "family": "Apiaceae",
        "description": "A slender flowering annual plant producing boat-shaped ridged seeds known for their earthy, warm, and distinctive savory aroma.",
        "ayurvedic_uses": [
            "Literally named 'Jeeraka' from the root meaning 'that which aids digestion'",
            "Balances Vata and Kapha while being neutral-to-gentle on Pitta",
            "Relieves flatulence, stimulates digestive enzymes, and promotes nutrient assimilation"
        ],
        "traditional_uses": [
            "Lightly roasted whole seeds added to warm buttermilk with black salt",
            "Boiled cumin water (Jeera water) sipped throughout the day for hydration and digestive ease",
            "Core aromatic foundation in dal tadka and vegetable sautés"
        ],
        "plant_parts_used": ["Seeds"],
        "precautions": [
            "Safe and beneficial in everyday dietary amounts",
            "Excessive therapeutic doses may modestly reduce blood glucose levels",
            "Avoid massive concentrated doses during pregnancy"
        ],
        "warnings": [
            "Monitor blood sugar when taking cumin supplements with anti-diabetic medications",
            "Not an alternative to medical therapy for chronic gastrointestinal disorders"
        ],
        "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=cuminum+cyminum+cumin+jeera"
    },
    {
        "common_name": "Mustard (Black Mustard)",
        "scientific_name": "Brassica nigra",
        "ayurvedic_name": "Sarshapa",
        "family": "Brassicaceae",
        "description": "An annual upright herb producing dark tiny pungent seeds and yellow flowers, cultivated across temperate and subtropical agricultural lands.",
        "ayurvedic_uses": [
            "Intensely sharp (Tikshna) and hot (Ushna), powerful for dispersing heavy Kapha and Vata",
            "Used traditionally in warming external poultices (Lepa) and medicated oils",
            "Stimulates circulation, sweating (Swedana), and localized heat sensation"
        ],
        "traditional_uses": [
            "Seeds popped in hot ghee or oil to release aromatic complexity into dishes",
            "Cold-pressed mustard oil used for traditional body and foot massages in winter",
            "Mustard seed foot baths used to draw warmth down to tired, cold extremities"
        ],
        "plant_parts_used": ["Seeds", "Seed oil"],
        "precautions": [
            "Can cause significant skin redness and burning if mustard plasters are left on too long",
            "Mustard oil contains erucic acid; check regional food regulations for internal consumption",
            "Aggravates Pitta; avoid in bleeding tendencies, ulcers, or high inflammation"
        ],
        "warnings": [
            "Do not leave mustard poultices on sensitive skin or on young children",
            "Seek medical guidance before using mustard oil internally where prohibited"
        ],
        "image_url": "https://images.unsplash.com/photo-1596040033229-a9821ebd058d?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=brassica+nigra+mustard+seeds"
    },
    {
        "common_name": "Nutmeg",
        "scientific_name": "Myristica fragrans",
        "ayurvedic_name": "Jatiphala",
        "family": "Myristicaceae",
        "description": "An evergreen tree indigenous to the Maluku Islands of Indonesia, bearing a yellow peach-like fruit containing a dark seed (nutmeg) surrounded by a red aril (mace).",
        "ayurvedic_uses": [
            "Aromatic, warming, and astringent; traditionally used as a mild sedative (Nidrajanana)",
            "Pacifies Vata and Kapha, steadying loose bowels (Grahani) and easing spasms",
            "Supports restful evening slumber and reproductive tonicity in minute amounts"
        ],
        "traditional_uses": [
            "Pinch of freshly grated nutmeg stirred into warm evening milk with saffron",
            "Used to flavor festive desserts, spiced breads, and savoury autumn dishes",
            "Topical paste made with water applied to the forehead for tension relief"
        ],
        "plant_parts_used": ["Dried seed kernel (nutmeg)", "Aril (mace / Javitri)"],
        "precautions": [
            "Use only in culinary pinches (under 1–2 grams); contains myristicin",
            "High doses (5+ grams) are toxic and can cause dizziness, hallucination, nausea, and tachycardia",
            "Strictly contraindicated in pregnancy due to potential uterine stimulation and toxicity"
        ],
        "warnings": [
            "Never consume large recreational doses of nutmeg; can cause severe poisoning",
            "Keep nutmeg out of reach of children and domestic pets"
        ],
        "image_url": "https://images.unsplash.com/photo-1509358271058-acd22cc93898?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=myristica+fragrans+nutmeg+jatiphala"
    },
    {
        "common_name": "Bael (Wood Apple / Bengal Quince)",
        "scientific_name": "Aegle marmelos",
        "ayurvedic_name": "Bilva",
        "family": "Rutaceae",
        "description": "A sacred deciduous tree with trifoliate leaves and large spherical hard-shelled fruits packed with aromatic orange pulp.",
        "ayurvedic_uses": [
            "One of the ten sacred roots of the foundational Dashamoola compound",
            "Unripe fruit is astringent, bitter, and drying; prime herb for regulating loose bowel movements (Sangrahi)",
            "Ripe fruit is mildly cooling, nourishing, and gentle on the digestive tract"
        ],
        "traditional_uses": [
            "Leaves offered in Shiva worship and chewed during spiritual fasting days",
            "Pulp of ripe fruit blended with water and jaggery into refreshing summer Bael Sharbat",
            "Unripe fruit powder taken with warm water for settling irritated intestines"
        ],
        "plant_parts_used": ["Fruit (ripe and unripe)", "Leaves", "Root bark"],
        "precautions": [
            "Unripe fruit is very binding; avoid in acute constipation or hard stools",
            "Excessive consumption of ripe fruit sharbat may produce heaviness or bloating",
            "Leaves may affect blood glucose levels"
        ],
        "warnings": [
            "Ensure proper hydration when taking astringent bowel-regulating herbs",
            "Consult a gastroenterologist for persistent chronic diarrhea or inflammatory bowel symptoms"
        ],
        "image_url": "https://images.unsplash.com/photo-1546548970-71785318a17b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=aegle+marmelos+bilva+bael"
    },
    {
        "common_name": "Jamun (Black Plum / Java Plum)",
        "scientific_name": "Syzygium cumini",
        "ayurvedic_name": "Jambu",
        "family": "Myrtaceae",
        "description": "A large evergreen tropical tree producing deep purple, astringent-sweet oval berries that stain the tongue purple.",
        "ayurvedic_uses": [
            "Astringent and cooling; historically renowned in Prameha (traditional metabolic balancing)",
            "Balances Kapha and Pitta doshas while toning intestinal membranes",
            "Seed powder traditionally utilized to help sustain balanced blood sugar levels"
        ],
        "traditional_uses": [
            "Fresh seasonal fruits eaten sprinkled with black salt and cumin",
            "Dried seed kernels pulverized into dietary powder for daily water intake",
            "Fruit vinegar (Jamun Sirka) taken as an appetizing traditional condiment"
        ],
        "plant_parts_used": ["Seeds", "Fruit pulp", "Stem bark"],
        "precautions": [
            "Eating unripe fruits or too many raw fruits can cause throat irritation and dryness",
            "Monitor blood sugar closely if combining seed powder with prescription diabetic medication",
            "Avoid consuming large amounts on an empty stomach"
        ],
        "warnings": [
            "Do not stop prescription insulin or oral hypoglycemics in favor of Jamun seed powder",
            "Consult a diabetologist for comprehensive glycemic management"
        ],
        "image_url": "https://images.unsplash.com/photo-1546548970-71785318a17b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=syzygium+cumini+jamun+ayurveda"
    },
    {
        "common_name": "Pomegranate",
        "scientific_name": "Punica granatum",
        "ayurvedic_name": "Dadima",
        "family": "Lythraceae",
        "description": "A fruit-bearing deciduous shrub producing thick-rinded red fruits packed with juicy edible jewel-like seed arils.",
        "ayurvedic_uses": [
            "Revered as a rare Tridoshic fruit that soothes Pitta without increasing Kapha or Vata",
            "Sweet-sour varieties are Hridya (nourishing to heart and emotions) and Deepana (digestive)",
            "Rind is powerfully astringent, traditionally used to support intestinal firmness"
        ],
        "traditional_uses": [
            "Fresh juice enjoyed for daily hydration, rich in natural polyphenols",
            "Dried wild seeds (Anardana) ground as a tart culinary seasoning in northern India",
            "Boiled rind decoctions used as traditional mouth and throat gargles"
        ],
        "plant_parts_used": ["Fruit arils", "Fruit rind", "Flowers", "Root bark"],
        "precautions": [
            "Rind decoctions are intensely astringent; overuse can cause constipation",
            "Pomegranate juice may inhibit CYP3A4 enzymes similarly to grapefruit, interacting with certain drugs",
            "Root bark contains alkaloids that can be toxic in high doses; avoid unsupervised use"
        ],
        "warnings": [
            "Check for drug interactions with statins or antihypertensive agents",
            "Avoid root bark preparations without qualified herbal oversight"
        ],
        "image_url": "https://images.unsplash.com/photo-1541344999736-83eca872f242?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=punica+granatum+pomegranate+ayurveda"
    },
    {
        "common_name": "Papaya",
        "scientific_name": "Carica papaya",
        "ayurvedic_name": "Erandakarkati",
        "family": "Caricaceae",
        "description": "A large fast-growing tree-like herb featuring palmate leaves and large oblong fruits filled with vibrant orange pulp and black seeds.",
        "ayurvedic_uses": [
            "Ripe fruit is sweet, cooling, and easily digestible, balancing Pitta and Vata",
            "Contains papain, a natural proteolytic enzyme traditionally recognized for digestive support",
            "Fresh leaf extract traditionally consumed during seasonal insect-borne fevers"
        ],
        "traditional_uses": [
            "Ripe fruit eaten fresh at breakfast to promote natural morning regularity",
            "Unripe green papaya cooked into savoury curries and salads (som tum)",
            "Crushed leaf juice taken in modest teaspoons to support blood platelet vitality"
        ],
        "plant_parts_used": ["Ripe fruit", "Unripe green fruit", "Leaves", "Seeds"],
        "precautions": [
            "Unripe papaya contains high latex concentrations and should be strictly avoided in pregnancy",
            "Excessive intake of papaya seeds may have anti-fertility effects",
            "Crushed leaf extract is extremely bitter and may cause nausea or stomach irritation"
        ],
        "warnings": [
            "Unripe papaya must not be consumed by pregnant individuals due to uterine contraction risks",
            "Do not substitute papaya leaves for emergency clinical care in severe dengue or thrombocytopenia"
        ],
        "image_url": "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=carica+papaya+ayurveda+uses"
    },
    {
        "common_name": "Castor Plant",
        "scientific_name": "Ricinus communis",
        "ayurvedic_name": "Eranda",
        "family": "Euphorbiaceae",
        "description": "A robust perennial shrub with bold palmate lobed leaves, prickly seed capsules, and mottled bean-like seeds.",
        "ayurvedic_uses": [
            "Proclaimed as the ultimate herb for subduing aggravated Vata dosha",
            "Castor oil (Eranda Taila) is the premier traditional purgative (Virechana) for clearing deep Ama",
            "Warm leaves applied topically for soothing joint stiffness and localized swelling"
        ],
        "traditional_uses": [
            "Warm castor oil packs placed over the lower abdomen or tight joints with a hot water bottle",
            "Castor oil massaged into eyebrows, eyelashes, and dry scalp for rich moisture",
            "A calibrated spoonful taken with warm ginger water under traditional detoxification programs"
        ],
        "plant_parts_used": ["Cold-pressed seed oil", "Roots", "Leaves"],
        "precautions": [
            "Raw castor seeds contain ricin, an extraordinarily lethal ribosome-inactivating protein; NEVER eat seeds",
            "Castor oil is a powerful stimulant laxative; can cause cramping and severe dehydration if overused",
            "Strictly contraindicated in pregnancy, appendicitis, intestinal obstruction, and inflammatory bowel disease"
        ],
        "warnings": [
            "CRITICAL: Whole seeds are violently toxic and potentially fatal if chewed or swallowed",
            "Never use castor oil internally to induce labor without hospital obstetricians present"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=ricinus+communis+castor+eranda"
    },
    {
        "common_name": "Senna",
        "scientific_name": "Senna alexandrina",
        "ayurvedic_name": "Swarnapatri",
        "family": "Fabaceae",
        "description": "A small bushy drought-tolerant shrub featuring pinnate leaves, yellow flowers, and flat oblong legumes containing seeds.",
        "ayurvedic_uses": [
            "Recognized as a classic Sukharechana (effective gentle laxative) in traditional texts",
            "Bitter and pungent taste with hot potency, expelling stagnant Pitta and Kapha wastes",
            "Used to stimulate peristalsis in short-term episodes of stubborn sluggishness"
        ],
        "traditional_uses": [
            "Dried leaflets brewed into occasional bedtime digestive teas",
            "Compounded with ginger or fennel to minimize intestinal cramping",
            "Formulated into traditional bowel-cleansing herbal powders"
        ],
        "plant_parts_used": ["Dried leaves (leaflets)", "Pods"],
        "precautions": [
            "Contains sennosides; intended strictly for short-term use (maximum 7 consecutive days)",
            "Chronic use can cause dependency, electrolyte depletion (potassium loss), and melanosis coli",
            "Contraindicated in undiagnosed abdominal pain, bowel obstruction, ulcerative colitis, and pregnancy"
        ],
        "warnings": [
            "Do not use for long-term daily regularity; can damage colon nerve endings",
            "Seek medical evaluation for chronic constipation rather than relying on stimulant laxatives"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=senna+alexandrina+swarnapatri"
    },
    {
        "common_name": "Psyllium (Isabgol)",
        "scientific_name": "Plantago ovata",
        "ayurvedic_name": "Ashwagol / Ishadgola",
        "family": "Plantaginaceae",
        "description": "A stemless annual herb with narrow linear leaves and dense flower spikes, producing tiny mucilaginous seeds.",
        "ayurvedic_uses": [
            "Sweet, cooling, and deeply lubricating (Snigdha), uniquely balancing for Vata and Pitta",
            "Acts as a gentle bulk-forming regulator suitable for both sluggish bowels and loose stools",
            "Creates a protective soothing coating over inflamed digestive membranes"
        ],
        "traditional_uses": [
            "1–2 teaspoons of seed husks stirred quickly into warm water or milk and drunk immediately",
            "Taken with curd/yogurt to help firm up occasional loose digestive conditions",
            "Added to gluten-free doughs to provide natural elasticity and fiber"
        ],
        "plant_parts_used": ["Seed husks (epidermis)", "Seeds"],
        "precautions": [
            "MUST ALWAYS be consumed with plenty of water (at least 250ml per dose) to prevent choking or intestinal blockage",
            "Take at least 2 hours before or after other medications, as it can delay drug absorption",
            "May cause temporary gas or bloating during initial days of fiber increase"
        ],
        "warnings": [
            "Do not consume dry without liquid; risk of esophageal obstruction",
            "Contraindicated in individuals with esophageal narrowing or bowel strictures"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=plantago+ovata+isabgol+psyllium"
    },
    {
        "common_name": "Babool (Gum Arabic Tree / Indian Acacia)",
        "scientific_name": "Vachellia nilotica",
        "ayurvedic_name": "Babbula",
        "family": "Fabaceae",
        "description": "A thorny moderate-sized tree with feathery bipinnate leaves, golden puffball flowers, and beaded seed pods.",
        "ayurvedic_uses": [
            "Profoundly Kashaya (astringent) and Grahi (binding), pacifying Kapha and Pitta",
            "Renowned classical tooth twig (Dantadhavana) for firming spongy gums and freshening breath",
            "Bark decoction used to tonify mucosal tissues and manage minor bleeding"
        ],
        "traditional_uses": [
            "Fresh slender twigs chewed into soft fibrous brushes for daily dental care",
            "Bark decoctions gargled for oral ulcers and sore gums",
            "Natural edible gum (Gond) pan-fried in ghee into nourishing winter laddoos"
        ],
        "plant_parts_used": ["Bark", "Gum", "Tender pods", "Leaves"],
        "precautions": [
            "High astringency can produce constipation if bark decoctions are swallowed in volume",
            "Use cautiously in dry Vata conditions",
            "Ensure twigs are harvested from clean rural trees away from road pollution"
        ],
        "warnings": [
            "Do not use sharp unchewed twigs that could lacerate gum tissues",
            "Seek professional dental evaluation for severe periodontal disease or tooth abscess"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=vachellia+nilotica+babool+acacia"
    },
    {
        "common_name": "Henna",
        "scientific_name": "Lawsonia inermis",
        "ayurvedic_name": "Madayantika",
        "family": "Lythraceae",
        "description": "A tall multi-stemmed desert shrub producing intensely fragrant white blossoms and leaves loaded with the natural dye lawsone.",
        "ayurvedic_uses": [
            "Strongly cooling (Shita) and Pitta-pacifying, renowned for drawing out trapped bodily heat",
            "Applied topically as a traditional remedy for burning feet sensations (Pada Daha)",
            "Natural hair conditioner that imparts rich copper tones and strengthens cuticles"
        ],
        "traditional_uses": [
            "Fresh or dried leaf paste applied to palms and soles for wedding celebrations and cooling",
            "Mixed with tea decoction and amla as a pure botanical hair dye",
            "Ground paste used on minor burns and heat blisters for immediate soothing"
        ],
        "plant_parts_used": ["Leaves", "Flowers", "Seeds"],
        "precautions": [
            "Intended primarily for external application; internal consumption of leaves is not recommended",
            "Persons with G6PD deficiency must strictly avoid henna, as lawsone can trigger acute hemolysis",
            "Ensure pure henna powder without synthetic paraphenylenediamine (PPD) black dyes"
        ],
        "warnings": [
            "Never use 'black henna' containing industrial coal-tar PPD; causes chemical burns and severe scarring",
            "Contraindicated in infants and individuals with glucose-6-phosphate dehydrogenase deficiency"
        ],
        "image_url": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=lawsonia+inermis+henna+plant"
    },
    {
        "common_name": "Vetiver (Khus)",
        "scientific_name": "Chrysopogon zizanioides",
        "ayurvedic_name": "Ushira",
        "family": "Poaceae",
        "description": "A densely tufted perennial clumping grass with deep spongy root networks possessing an earthy, woody, and intensely cooling aroma.",
        "ayurvedic_uses": [
            "Hailed as supreme Shita (cooling) and Dahaprashamana (fever-heat relieving) botanical",
            "Pacifies burning Pitta, cools emotional agitation, and quenches intense thirst (Trishna)",
            "Applied topically in classical sandalwood-vetiver cooling pastes during high summer"
        ],
        "traditional_uses": [
            "Roots woven into window blinds and desert cooler mats, sprayed with water to perfume and chill the breeze",
            "Drinking water steeped with clean vetiver root bundles for sweet, earthy summer refreshment",
            "Khus essential oil ('oil of tranquility') worn in perfumery and used in relaxing massage"
        ],
        "plant_parts_used": ["Fibrous roots", "Root essential oil"],
        "precautions": [
            "Profoundly cooling; may aggravate cold-congested Kapha or Vata chills if overused in winter",
            "Ensure roots used for steeping water are food-grade and thoroughly cleaned",
            "Dilute essential oil before skin contact"
        ],
        "warnings": [
            "Do not consume concentrated vetiver fragrance oils internally",
            "Not a substitute for emergency rehydration fluids in severe heat stroke"
        ],
        "image_url": "https://images.unsplash.com/photo-1514733670139-4d87a1941d55?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=chrysopogon+zizanioides+vetiver+ushira"
    },
    {
        "common_name": "Indian Sandalwood",
        "scientific_name": "Santalum album",
        "ayurvedic_name": "Chandana",
        "family": "Santalaceae",
        "description": "A prized hemiparasitic evergreen tree indigenous to southern India, whose heartwood and essential oil possess a sacred creamy-woody scent.",
        "ayurvedic_uses": [
            "Premier Medhya and cooling Pitta-soothing botanical across classical scriptures",
            "Bitter, sweet, and intensely Shita (cooling), clearing mental agitation and heat flare-ups",
            "Applied to the forehead (Ajna chakra) to settle thoughts, headaches, and summer heat"
        ],
        "traditional_uses": [
            "Heartwood rubbed with water on a stone slab to create fresh fragrant tilak paste",
            "Pure paste mixed with rose water for calming skin redness, acne, and prickly heat",
            "Burned as sacred incense in temple sanctums and meditation sanctuaries"
        ],
        "plant_parts_used": ["Heartwood", "Heartwood essential oil"],
        "precautions": [
            "Ensure ethical sourcing from government-regulated plantations; wild trees are heavily protected",
            "Pure sandalwood is cooling and dry; use with moisturizing carriers on very dry skin",
            "Internal use of sandalwood oil should strictly occur under physician supervision"
        ],
        "warnings": [
            "High internal doses of sandalwood oil can irritate the kidneys and urinary tract",
            "Beware of widespread synthetic or chemical adulterations in market oils"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=santalum+album+sandalwood+chandana"
    },
    {
        "common_name": "Camphor Tree",
        "scientific_name": "Cinnamomum camphora",
        "ayurvedic_name": "Karpura",
        "family": "Lauraceae",
        "description": "A magnificent broad-leaved evergreen tree whose wood and leaves yield pure aromatic crystalline camphor upon steam distillation.",
        "ayurvedic_uses": [
            "Unique dual nature: cooling to the sensation yet pungent, sharp, and clearing to Kapha channels",
            "Acts as a cardiac and respiratory stimulant (Hridya) in minute classical doses",
            "Opens congested nasal passages, clears mental fog, and soothes itchiness"
        ],
        "traditional_uses": [
            "Edible camphor (Pachha Karpooram) added in micro-pinches to temple sweet rice (Tirupati laddu)",
            "Dissolved in coconut oil and rubbed onto the chest for seasonal breathing ease",
            "Burned in sacred aarti lamps for visual clarity and energetic purification"
        ],
        "plant_parts_used": ["Crystalline sublimated resin", "Wood", "Leaves"],
        "precautions": [
            "CRITICAL: Synthetic industrial camphor is toxic and MUST NEVER be swallowed",
            "Only authenticated botanical edible grade (Bhimseni / Pachha Karpooram) can be consumed, and only in microscopic pinches",
            "Camphor is easily absorbed through broken skin and mucous membranes; keep away from children"
        ],
        "warnings": [
            "Never ingest non-edible ritual camphor blocks; can cause seizures and fatal poisoning in children",
            "Keep all camphor products securely out of reach of small children"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=cinnamomum+camphora+karpura+ayurveda"
    },
    {
        "common_name": "Nagkesar (Ceylon Ironwood / Cobra's Saffron)",
        "scientific_name": "Mesua ferrea",
        "ayurvedic_name": "Nagakeshara",
        "family": "Calophyllaceae",
        "description": "A majestic evergreen tropical tree producing fragrant white flowers with a central mass of golden-yellow stamens.",
        "ayurvedic_uses": [
            "Astringent, bitter, and warming; traditionally indicated for managing bleeding tendencies (Raktapitta)",
            "Member of the classical aromatic Chaturjata group, enhancing digestion and metabolic agni",
            "Used to pacify Kapha and Pitta while supporting uterine tone and respiratory clarity"
        ],
        "traditional_uses": [
            "Dried floral stamens formulated into classical remedies for hemorrhoids and bleeding gums",
            "Floral paste combined with butter applied topically for burning sensations",
            "Flowers dried and used in potpourri, cosmetics, and incense blends"
        ],
        "plant_parts_used": ["Dried flower buds and stamens"],
        "precautions": [
            "Astringent and drying; may cause mild constipation if taken without adequate fluids",
            "Avoid in cases of chronic severe constipation or dry Vata depletion",
            "Consult a practitioner before taking during pregnancy"
        ],
        "warnings": [
            "Do not use in place of medical intervention for unexplained rectal or internal bleeding",
            "Verify botanical purity as substitutes are common in commercial markets"
        ],
        "image_url": "https://images.unsplash.com/photo-1550950158-d0d960dff51b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=mesua+ferrea+nagkesar"
    },
    {
        "common_name": "Lodhra",
        "scientific_name": "Symplocos racemosa",
        "ayurvedic_name": "Lodhra",
        "family": "Symplocaceae",
        "description": "An evergreen tree with dark grey wrinkled bark and fragrant yellow flowers, native to the evergreen forests of northern and eastern India.",
        "ayurvedic_uses": [
            "Celebrated for its Kashaya (astringent) taste and Shita (cooling) potency",
            "Foremost classical herb for women's reproductive health, supporting uterine mucosa and balanced cycles",
            "Topically applied to firm tissues, soothe skin inflammation, and support wound astringency"
        ],
        "traditional_uses": [
            "Bark decoctions taken during heavy menstrual flow under clinical supervision",
            "Bark powder mixed with rose water for clearing oily acne-prone skin",
            "Used in classical eye washes (Parisheka) for soothing ocular heat"
        ],
        "plant_parts_used": ["Stem bark"],
        "precautions": [
            "Powerfully astringent; can cause mild constipation and dryness if taken excessively",
            "Take with plenty of warm water or honey to moderate dryness",
            "Use during pregnancy only under experienced clinical direction"
        ],
        "warnings": [
            "Seek medical investigation for abnormal or post-menopausal uterine bleeding",
            "Not a substitute for obstetric care in pregnancy complications"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=symplocos+racemosa+lodhra"
    },
    {
        "common_name": "Ashoka Tree",
        "scientific_name": "Saraca asoca",
        "ayurvedic_name": "Ashoka",
        "family": "Fabaceae",
        "description": "A sacred rainforest tree with luxuriant foliage and fragrant heavy clusters of bright orange-scarlet flowers.",
        "ayurvedic_uses": [
            "Its name literally signifies 'that which removes grief or sorrow'",
            "Foremost traditional uterine tonic, balancing Pitta and Kapha in female physiology",
            "Key ingredient in classical Ashokarishta, supporting comfortable menstrual cycles"
        ],
        "traditional_uses": [
            "Bark boiled in milk and water (Ksheerapaka) for menstrual discomfort",
            "Planted near traditional courtyards and temples for tranquility and sacred shade",
            "Flowers pounded into soothing pastes for internal heat balancing"
        ],
        "plant_parts_used": ["Stem bark", "Flowers", "Seeds"],
        "precautions": [
            "Astringent taste may cause mild constipation in Vata-prone individuals",
            "Ensure genuine Saraca asoca bark; Polyalthia longifolia (false ashoka) is frequently adulterated",
            "Avoid during pregnancy unless directed by an obstetric Vaidya"
        ],
        "warnings": [
            "Crucial to verify authenticity as the true Ashoka tree is an endangered medicinal species",
            "Consult a gynecologist for persistent pelvic pain or menstrual irregularities"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=saraca+asoca+true+ashoka+tree"
    },
    {
        "common_name": "Pippali (Indian Long Pepper)",
        "scientific_name": "Piper longum",
        "ayurvedic_name": "Pippali",
        "family": "Piperaceae",
        "description": "A slender climbing vine with glossy heart-shaped leaves and dense cylindrical spike inflorescences of fused tiny fruits.",
        "ayurvedic_uses": [
            "Cornerstone of the Trikatu formulation and a profound Rasayana for Pranavaha Srotas (respiratory tract)",
            "Pungent initially with sweet post-digestive effect (Madhura Vipaka), balancing Kapha and Vata without severely irritating Pitta",
            "Kindles Agni, clears sticky Ama, and aids in deep tissue rejuvenation (Vardhamana Pippali)"
        ],
        "traditional_uses": [
            "Pinch of powdered spike taken with raw honey for seasonal coughs and throat congestion",
            "Simmered in cow's milk for traditional vitality tonics and respiratory recovery",
            "Added to medicinal ghee and winter spice preserves"
        ],
        "plant_parts_used": ["Dried fruiting spikes", "Roots (Pippalimoola)"],
        "precautions": [
            "Heating; prolonged high doses may eventually aggravate Pitta",
            "Increases systemic absorption of prescription medications via piperine",
            "Avoid excessive use in active gastritis, acid reflux, or peptic ulcers"
        ],
        "warnings": [
            "Exercise caution if taking pharmaceuticals with a narrow therapeutic index",
            "Do not consume large doses continuously without structured breaks"
        ],
        "image_url": "https://images.unsplash.com/photo-1508746829417-e6f548d8d6ed?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=piper+longum+pippali+long+pepper"
    },
    {
        "common_name": "Chitraka (Ceylon Leadwort)",
        "scientific_name": "Plumbago zeylanica",
        "ayurvedic_name": "Chitraka",
        "family": "Plumbaginaceae",
        "description": "A rambling perennial subshrub featuring bright green leaves and terminal racemes of starry white flowers with glandular sticky calyces.",
        "ayurvedic_uses": [
            "Famous for its ferocious digestive fire (Deepana) qualities, named after fire/Agni",
            "Instantly burns accumulated toxins (Ama) and clears sluggish Kapha coldness",
            "Foundational herb in classical formulas such as Chitrakadi Vati"
        ],
        "traditional_uses": [
            "Root powder taken in micro-doses before meals to awaken appetite",
            "Formulated into gut cleansing and metabolic clearing pills",
            "Mixed with buttermilk to temper its intense heating potency"
        ],
        "plant_parts_used": ["Roots"],
        "precautions": [
            "Extremely hot and sharp (Ushna and Tikshna); can cause burning sensations or stomach irritation",
            "STRICTLY contraindicated during pregnancy as plumbagin is a potent abortifacient and uterine stimulant",
            "Avoid in active ulcers, bleeding disorders, high Pitta, or severe gastritis"
        ],
        "warnings": [
            "NEVER consume during pregnancy; has documented abortifacient effects",
            "Take only in minute calibrated doses under qualified clinical direction"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=plumbago+zeylanica+chitraka"
    },
    {
        "common_name": "Gokshura (Small Caltrops / Puncture Vine)",
        "scientific_name": "Tribulus terrestris",
        "ayurvedic_name": "Gokshura",
        "family": "Zygophyllaceae",
        "description": "A low-growing prostrate annual weed with pinnate leaves, yellow flowers, and hard woody five-angled burrs equipped with sharp spines.",
        "ayurvedic_uses": [
            "A member of Dashamoola and a celebrated Rasayana for urinary and reproductive wellness (Vrishya)",
            "Sweet in taste and cooling in potency, gently pacifying all three doshas",
            "Traditionally used to clear urinary discomfort and support vitality and stamina"
        ],
        "traditional_uses": [
            "Boiled into water as a soothing diuretic tea during hot weather",
            "Combined with Ashwagandha and Shatavari in sports and vitality regimens",
            "Used in classical Gokshuradi Guggulu for joint and urinary fluid comfort"
        ],
        "plant_parts_used": ["Spiny fruits (burrs)", "Roots", "Whole plant"],
        "precautions": [
            "Has mild diuretic properties; ensure adequate daily fluid intake",
            "May influence hormone pathways; use with care in hormone-sensitive conditions",
            "Avoid unsupervised use during pregnancy and lactation"
        ],
        "warnings": [
            "Spiny burrs are a physical hazard for barefoot walkers and pets",
            "Seek medical care for severe urinary tract pain, blood in urine, or acute retention"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=tribulus+terrestris+gokshura"
    },
    {
        "common_name": "Kaunch Beej (Velvet Bean)",
        "scientific_name": "Mucuna pruriens",
        "ayurvedic_name": "Kapikacchu",
        "family": "Fabaceae",
        "description": "A vigorous climbing tropical legume producing hanging clusters of pods covered with velvety stinging hairs that contain shiny seeds.",
        "ayurvedic_uses": [
            "Premier classical Vrishya (reproductive tonic) and Balya (strengthener)",
            "Sweet and bitter in taste, unctuous and warming, deeply pacifying aggravated Vata",
            "Natural botanical source of L-DOPA, traditionally recognized for steadying tremors and lifting spirit"
        ],
        "traditional_uses": [
            "Purified seeds ground into powder and taken with warm milk, ghee, and raw cane sugar",
            "Included in rejuvenating tonics for muscle endurance and vitality",
            "Formulated into nourishing pastes for nervous system balance"
        ],
        "plant_parts_used": ["Purified seeds"],
        "precautions": [
            "Raw seeds contain anti-nutrients and must undergo traditional boiling/purification before use",
            "Rich in L-DOPA; can interact significantly with MAO inhibitors and Parkinson's prescription medications",
            "May cause nausea, headache, or rapid heart rate if taken in uncalibrated high doses"
        ],
        "warnings": [
            "Pod hairs cause extreme skin itching and should never be touched with bare hands",
            "Do not combine with synthetic dopaminergic or antidepressant drugs without medical oversight"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=mucuna+pruriens+kapikacchu"
    },
    {
        "common_name": "Nirgundi (Five-Leaved Chaste Tree)",
        "scientific_name": "Vitex negundo",
        "ayurvedic_name": "Nirgundi",
        "family": "Lamiaceae",
        "description": "A large aromatic shrub with palmately compound 3-to-5 foliate leaves, bluish-purple flowers, and black berries, native to stream banks.",
        "ayurvedic_uses": [
            "Name signifies 'that which protects the body from ailments'",
            "Foremost Vata-pacifying herb for soothing joint pain, swelling, and muscle stiffness",
            "Formulated into Nirgundi Taila, a staple medicated oil for musculoskeletal comfort"
        ],
        "traditional_uses": [
            "Leaves heated in castor oil and applied as a warm poultice to stiff joints",
            "Boiled leaves added to bath water for soothing postpartum or tired body aches",
            "Fresh leaf smoke inhaled gently for seasonal headache relief in folk traditions"
        ],
        "plant_parts_used": ["Leaves", "Roots", "Seeds"],
        "precautions": [
            "Pungent and heating; can aggravate Pitta dosha if taken internally in large quantities",
            "May interact with hormonal therapies, oral contraceptives, or dopamine agonists",
            "Avoid internal consumption during pregnancy and lactation"
        ],
        "warnings": [
            "External application is preferred in home care; internal use requires professional direction",
            "Seek medical attention for severe trauma or acute joint effusions"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=vitex+negundo+nirgundi"
    },
    {
        "common_name": "Bakuchi (Psoralea Seeds)",
        "scientific_name": "Cullen corylifolium",
        "ayurvedic_name": "Bakuchi",
        "family": "Fabaceae",
        "description": "An annual herb producing purplish flowers and small black kidney-shaped seeds, famous as the source of botanical bakuchiol and psoralens.",
        "ayurvedic_uses": [
            "Classical herb of choice for Kustha (chronic skin conditions) and Shvitra (pigmentation balance)",
            "Pungent and bitter in taste, hot in potency, pacifying Kapha and Vata",
            "Stimulates melanin synthesis when exposed to gentle morning sun under traditional supervision"
        ],
        "traditional_uses": [
            "Purified seed paste applied topically followed by brief exposure to mild early morning sunlight",
            "Bakuchiol extracts used in modern clean skincare as a gentle plant alternative to retinol",
            "Compounded with haridra and neem for holistic dermal care"
        ],
        "plant_parts_used": ["Seeds", "Seed oil"],
        "precautions": [
            "Contains potent psoralens that cause marked photosensitivity; improper sun exposure can cause blistering burns",
            "Must be traditionally purified before any therapeutic application",
            "Contraindicated during pregnancy, liver disorders, and in individuals with sun allergy"
        ],
        "warnings": [
            "Overexposure to sun after Bakuchi application can result in severe second-degree phototoxic burns",
            "Never use on skin before tanning beds or intense midday sun"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=cullen+corylifolium+bakuchi"
    },
    {
        "common_name": "Karanja (Indian Beech)",
        "scientific_name": "Pongamia pinnata",
        "ayurvedic_name": "Karanja",
        "family": "Fabaceae",
        "description": "A medium-sized canopy tree with glossy pinnate foliage, pink-white fragrant flowers, and thick woody seed pods.",
        "ayurvedic_uses": [
            "Bitter, pungent, and astringent; highly valued for cleansing Kapha and Pitta skin flare-ups",
            "Karanja oil is a classic external remedy for soothing itchy skin, eczema, and scalp dandruff",
            "Twigs used traditionally as an antibacterial dental cleansing twig"
        ],
        "traditional_uses": [
            "Seed oil applied topically to soothe resistant skin patches and fungal concerns",
            "Leaf decoctions used for antiseptic washes on minor abrasions",
            "Foliage used as green manure to repel soil pests in organic farming"
        ],
        "plant_parts_used": ["Seed oil", "Bark", "Leaves", "Seeds"],
        "precautions": [
            "Karanja oil is strictly for external use and is toxic if swallowed",
            "Can cause skin irritation or contact dermatitis in high concentrations; dilute in sesame oil",
            "Avoid contact with eyes and open mucous membranes"
        ],
        "warnings": [
            "DO NOT INGEST Karanja oil; contains toxic furanoflavonoids (karanjin)",
            "Keep oil stored safely away from children and household pets"
        ],
        "image_url": "https://images.unsplash.com/photo-1448375240586-882707db888b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=pongamia+pinnata+karanja"
    },
    {
        "common_name": "Kantakari (Yellow-Berried Nightshade)",
        "scientific_name": "Solanum virginianum",
        "ayurvedic_name": "Kantakari",
        "family": "Solanaceae",
        "description": "A prickly, diffuse prostrate herb with zigzag stems armed with bright yellow spines, purple flowers, and striped yellow berries.",
        "ayurvedic_uses": [
            "Member of the classical Dashamoola and Kantakaryavaleha formulations",
            "Renowned Kasahara (cough reliever) and Shvasahara (breathing eases), dispersing thick sticky Kapha",
            "Pungent and bitter in taste, with hot potency that dissolves respiratory congestion"
        ],
        "traditional_uses": [
            "Whole herb boiled into decoctions with ginger and long pepper for chest cold relief",
            "Dried fruit smoke gently inhaled in folk remedies for tooth discomfort",
            "Formulated into soothing herbal syrups for seasonal broncho-respiratory balance"
        ],
        "plant_parts_used": ["Whole plant (Panchanga)", "Fruits", "Roots"],
        "precautions": [
            "Contains solasodine alkaloids; avoid high unsupervised doses",
            "Contraindicated during pregnancy due to potential uterine stimulating actions",
            "Sharp spines require careful handling when harvesting"
        ],
        "warnings": [
            "Do not consume raw unverified nightshade berries",
            "Seek emergency care for acute asthma attacks or severe respiratory compromise"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=solanum+virginianum+kantakari"
    },
    {
        "common_name": "Dhataki (Fire-Flame Bush)",
        "scientific_name": "Woodfordia fruticosa",
        "ayurvedic_name": "Dhataki",
        "family": "Lythraceae",
        "description": "A spreading deciduous shrub that erupts in clusters of brilliant scarlet-red flowers along its branches.",
        "ayurvedic_uses": [
            "Essential classical fermenting agent used in creating all authentic Asavas and Arishtas",
            "Flowers naturally harbor wild yeasts that drive traditional biotransformation and fermentation",
            "Astringent and cooling; supports healthy mucosal firmness and balances Pitta and Kapha"
        ],
        "traditional_uses": [
            "Dried flowers added to classical earthen fermentation vats with herbal decoctions and jaggery",
            "Pounded flowers used in dusting powders for minor surface cuts",
            "Used traditionally in women's tonics for reproductive comfort"
        ],
        "plant_parts_used": ["Dried flowers"],
        "precautions": [
            "Astringent nature can induce mild constipation if taken alone in high amounts",
            "Ensure flowers are properly dried and free from storage mold",
            "Avoid in cases of severe intestinal dryness"
        ],
        "warnings": [
            "Fermented preparations containing Dhataki generate self-generated alcohol (usually 5–10%); caution for recovering alcoholics",
            "Seek medical guidance before giving fermented herbal wines to children"
        ],
        "image_url": "https://images.unsplash.com/photo-1550950158-d0d960dff51b?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=woodfordia+fruticosa+dhataki"
    },
    {
        "common_name": "Rasna",
        "scientific_name": "Pluchea lanceolata",
        "ayurvedic_name": "Rasna",
        "family": "Asteraceae",
        "description": "A fast-growing erect herbaceous shrub with lanceolate leaves and purple-pink composite flower heads, flourishing in semi-arid zones.",
        "ayurvedic_uses": [
            "Celebrated as a prime Vata-pacifying herb specifically targeted for joint comfort (Amavatahara)",
            "Bitter in taste, warming in potency, supporting flexible movement in cold weather",
            "Key botanical in the famous classical joint decoction Rasnasaptaka Kwatha"
        ],
        "traditional_uses": [
            "Decoction sipped with a pinch of dry ginger for morning joint stiffness",
            "Formulated into massage oils for lower back and hip comfort",
            "Used in classical basti (medicated enema) formulations in Panchakarma"
        ],
        "plant_parts_used": ["Leaves", "Roots"],
        "precautions": [
            "Warming and drying; balance with unctuous herbs like sesame oil or ghee in high Vata states",
            "Can slightly aggravate Pitta heat if taken in excess during hot summer months",
            "Safety in pregnancy has not been established"
        ],
        "warnings": [
            "Verify botanical source as several unrelated plants share the vernacular name Rasna",
            "Do not substitute for rheumatologic medications without consulting your specialist"
        ],
        "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=pluchea+lanceolata+rasna"
    },
    {
        "common_name": "Tagara (Indian Valerian)",
        "scientific_name": "Valeriana jatamansi",
        "ayurvedic_name": "Tagara",
        "family": "Caprifoliaceae",
        "description": "A tufted hairy perennial herb native to the temperate Himalayas, possessing thick aromatic horizontal rhizomes.",
        "ayurvedic_uses": [
            "Renowned classical Nidrajanana (sleep-inducing) and calming herb",
            "Sweet, bitter, and pungent in taste with warming potency, subduing agitated Vata and Kapha",
            "Helps ease nervous restlessness, muscle spasms, and racing evening thoughts"
        ],
        "traditional_uses": [
            "Small dose of rhizome powder taken with warm milk 30 minutes before sleep",
            "Included in calming cranial herbal oils",
            "Used historically as a soothing incense herb"
        ],
        "plant_parts_used": ["Rhizomes and roots"],
        "precautions": [
            "May cause morning grogginess or vivid dreams if taken in excessive doses",
            "Do not combine with prescription sedatives, sleeping pills, or alcohol",
            "Do not operate motor vehicles or heavy machinery after taking Tagara"
        ],
        "warnings": [
            "Avoid during pregnancy and lactation",
            "Consult a physician before using if taking prescription central nervous system depressants"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=valeriana+jatamansi+tagara"
    },
    {
        "common_name": "Jatamansi (Spikenard)",
        "scientific_name": "Nardostachys jatamansi",
        "ayurvedic_name": "Jatamansi",
        "family": "Caprifoliaceae",
        "description": "An endangered alpine Himalayan herb producing fragrant hairy rhizomes resembling knotted hair tresses.",
        "ayurvedic_uses": [
            "Sublime Medhya Rasayana celebrated for its peaceful, stabilizing effect on the mind (Manas)",
            "Cooling in potency unlike Valerian, pacifying all three doshas, especially Pitta and Vata",
            "Supports peaceful sleep, emotional poise, and mental focus without daytime sluggishness"
        ],
        "traditional_uses": [
            "Root powder taken in minute pinches with ghee and honey for meditation support",
            "Steeped into nourishing hair oils to soothe both the scalp and busy thoughts",
            "Burned as precious temple incense for deep spiritual serenity"
        ],
        "plant_parts_used": ["Rhizomes and roots"],
        "precautions": [
            "Critically endangered species; ensure products come from certified ethical and cultivated sources",
            "May lower blood pressure; monitor if prone to hypotension",
            "Avoid unsupervised use during pregnancy and lactation"
        ],
        "warnings": [
            "Do not harvest or purchase wild poached Himalayan Jatamansi",
            "Not an alternative to medical psychiatric therapy for clinical depression or psychosis"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=nardostachys+jatamansi+spikenard"
    },
    {
        "common_name": "Ativisha (Indian Atees)",
        "scientific_name": "Aconitum heterophyllum",
        "ayurvedic_name": "Ativisha",
        "family": "Ranunculaceae",
        "description": "A rare perennial alpine herb with tuberous roots and showy bluish-white flowers, renowned for non-toxic aconite properties.",
        "ayurvedic_uses": [
            "Unlike other aconites, Ativisha is traditionally classified as non-poisonous (Nirvisha)",
            "Intensely bitter and pungent, revered for kindle-digestion (Deepana) and fever-balancing actions",
            "Used traditionally in Balachaturbhadra Churna for gentle pediatric digestive comfort"
        ],
        "traditional_uses": [
            "Administered in minute measured micro-pinches with honey for settling children's digestive upsets",
            "Used classically to counteract metabolic toxins and sluggish seasonal chills",
            "Formulated into traditional fever balance compounds"
        ],
        "plant_parts_used": ["Tuberous roots"],
        "precautions": [
            "Must never be confused with toxic aconite species (such as Aconitum ferox / Vatsanabha)",
            "Administer strictly under the prescription of an experienced Ayurvedic clinician",
            "Endangered species; use with high conservation awareness"
        ],
        "warnings": [
            "CRITICAL: Mistaking poisonous aconites for Ativisha can cause fatal cardiac toxicity",
            "Never harvest or consume wild unverified aconite roots"
        ],
        "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&q=80",
        "video_url": "https://www.youtube.com/results?search_query=aconitum+heterophyllum+ativisha"
    }
]

def main():
    target_path = os.path.join(os.path.dirname(__file__), "..", "data", "plants.json")
    target_path = os.path.abspath(target_path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(PLANTS, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {len(PLANTS)} plants in {target_path}")

if __name__ == "__main__":
    main()
