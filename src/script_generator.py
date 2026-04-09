"""
Video Script Generator
Generates structured YouTube video scripts for faceless channels.
Supports 4 niches: Ancient, Ocean, Space, Unsolved
Auto-detects niche from topic keywords.

Author: Muhammad Saboor
"""

import os
import json
import re

SCRIPTS_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos/scripts"
os.makedirs(SCRIPTS_DIR, exist_ok=True)


# ── Niche detection ──────────────────────────────────────────────

NICHE_KEYWORDS = {
    "ancient": ["ancient", "ruins", "pyramid", "temple", "archaeol", "civiliz", "artifact", "impossible", "giza", "egypt"],
    "ocean": ["ocean", "sea", "underwater", "deep sea", "marine", "aquatic", "ship", "bermuda", "abyss", "wave"],
    "space": ["space", "universe", "cosmic", "star", "planet", "galaxy", "alien", "signal", "dark energy"],
    "unsolved": ["unsolved", "mystery", "disappear", "crime", "murder", "missing", "unexplained", "strange", "haunt"],
}


def detect_niche(topic):
    """Auto-detect the best niche from topic keywords."""
    t = topic.lower()
    scores = {}
    for niche, keywords in NICHE_KEYWORDS.items():
        scores[niche] = sum(1 for kw in keywords if kw in t)
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "ancient"


def extract_count(topic):
    """Extract the number from the topic (e.g. '7' from '7 Ancient Discoveries')."""
    for word in topic.split():
        if word.isdigit():
            return int(word)
    return 7


# ── Script templates ─────────────────────────────────────────────

TEMPLATES = {

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # ANCIENT DISCOVERIES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "ancient": {
        "intro_hook": "What if everything we thought we knew about ancient history was wrong? From impossible constructions to mysterious artifacts that defy modern science, these discoveries continue to baffle researchers and historians around the world.",
        "outro": "These ancient discoveries remind us that our ancestors were far more capable and intelligent than we often give them credit for. Each of these mysteries pushes back the boundaries of what we thought was possible in the ancient world. If you found this video fascinating, make sure to like and subscribe for more explorations into the unknown. What ancient mystery do you find most puzzling? Let us know in the comments below.",
        "items": [
            {
                "title": "The Antikythera Mechanism",
                "narration": "Discovered in a shipwreck off the coast of Greece in 1901, the Antikythera Mechanism is often called the world's first analog computer. This intricate bronze device, dating back to around 100 BC, contains over 30 interlocking gears designed to predict astronomical events, eclipses, and even the timing of the ancient Olympic Games. The level of technology found in this mechanism wouldn't be seen again for over a thousand years. How did the ancient Greeks develop something this advanced? Scientists are still trying to figure that out.",
                "footage_query": "ancient greek ruins ocean underwater archaeology",
            },
            {
                "title": "The Nazca Lines",
                "narration": "Stretching across the desert plains of southern Peru, the Nazca Lines are a series of massive geoglyphs etched into the earth over 2,000 years ago. These enormous designs depict animals, plants, and geometric shapes, some spanning over 300 meters in length. The most puzzling aspect is that these figures can only be fully appreciated from the air, yet they were created centuries before human flight. Who were they made for? And how did the Nazca people achieve such precision without being able to see their work from above?",
                "footage_query": "desert aerial landscape ancient peru mysterious",
            },
            {
                "title": "The Piri Reis Map",
                "narration": "Created in 1513 by Ottoman admiral Piri Reis, this map depicts the coastlines of South America and what appears to be Antarctica with remarkable accuracy. The problem? Antarctica wasn't officially discovered until 1820, over 300 years later. Even more astonishing, the map seems to show the continent's coastline without its ice cover, a state that hasn't existed for at least 6,000 years. Piri Reis claimed he based his map on older source maps, some dating back to the time of Alexander the Great. If true, who mapped Antarctica thousands of years ago?",
                "footage_query": "ancient map compass navigation ocean exploration",
            },
            {
                "title": "Gobekli Tepe",
                "narration": "Located in southeastern Turkey, Gobekli Tepe is a monumental complex of massive stone pillars arranged in circles, some weighing up to 20 tons. What makes this site extraordinary is its age. Built around 11,600 years ago, it predates Stonehenge by over 6,000 years and was constructed before humans are believed to have developed agriculture or even pottery. The carvings on the pillars depict animals and abstract symbols with incredible detail. How did hunter-gatherers organize the labor and expertise to build something this complex?",
                "footage_query": "ancient stone temple ruins pillars archaeology mysterious",
            },
            {
                "title": "The Voynich Manuscript",
                "narration": "This mysterious book, written in the early 15th century, is filled with colorful illustrations of unidentifiable plants, astronomical diagrams, and hundreds of pages of text written in a completely unknown language or code. Despite decades of effort by the world's top cryptographers and linguists, including World War Two codebreakers, no one has ever been able to decipher a single word. Carbon dating confirms its authenticity, ruling out a modern hoax. Who wrote it, and what secrets does it contain? We may never know.",
                "footage_query": "ancient book manuscript mysterious old library",
            },
            {
                "title": "The Baghdad Battery",
                "narration": "Found near Baghdad, Iraq, these clay jars dating back to around 250 BC contain copper cylinders and iron rods. When filled with an acidic solution like vinegar, they can generate a small electric current. Were the ancient Parthians using electricity nearly 2,000 years before the modern battery was invented? Some researchers believe these devices were used for electroplating gold onto silver objects. Others argue they were simply storage vessels. The debate continues, but the possibility that ancient civilizations understood electricity is remarkable.",
                "footage_query": "ancient artifacts clay pottery museum archaeology",
            },
            {
                "title": "The Great Pyramid of Giza",
                "narration": "Standing for over 4,500 years, the Great Pyramid remains one of the most precisely engineered structures ever built. Its base is level to within just 2 centimeters across 230 meters. It was aligned to true north with an accuracy of just 3 arc minutes. The pyramid contains an estimated 2.3 million stone blocks, each weighing an average of 2.5 tons, with some granite blocks in the King's Chamber weighing up to 80 tons. Even with modern technology, replicating this feat would be extraordinarily difficult. How did the ancient Egyptians achieve such precision with copper tools and manual labor?",
                "footage_query": "pyramids egypt desert sunset cinematic aerial",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # OCEAN MYSTERIES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "ocean": {
        "intro_hook": "We have explored more of the surface of Mars than the floor of our own oceans. Covering over 70 percent of the planet, the deep sea remains Earth's last true frontier, hiding secrets that challenge our understanding of nature, history, and life itself. These are the most terrifying and unexplained discoveries from beneath the waves.",
        "outro": "The ocean covers more than two-thirds of our planet, yet we have mapped less than 20 percent of the seafloor in detail. Every year, new expeditions reveal creatures, structures, and phenomena that we never imagined could exist. What else is hiding in the darkness below? If this video left you amazed, hit like and subscribe for more deep dives into the unknown. Tell us in the comments, which ocean mystery disturbs you the most?",
        "items": [
            {
                "title": "The Bloop",
                "narration": "In 1997, the National Oceanic and Atmospheric Administration recorded an ultra low frequency sound in the southern Pacific Ocean. Named the Bloop, it was so powerful that it was detected by sensors over 5,000 kilometers apart. The sound matched the profile of a living creature, but to produce it, the animal would need to be far larger than any known species, including the blue whale. Scientists later attributed it to an icequake, but many remain unconvinced. What exactly made this sound in the darkest depths of our ocean?",
                "footage_query": "dark deep ocean sonar submarine underwater",
            },
            {
                "title": "The Baltic Sea Anomaly",
                "narration": "In 2011, a Swedish diving team discovered a mysterious circular object resting on the Baltic Sea floor at a depth of 90 meters. The structure spans roughly 60 meters across and features what appear to be stairways, ramps, and corridors. Sonar imaging revealed a 300 meter trail behind it, as if it had skidded across the ocean floor. Some claim it resembles the Millennium Falcon from Star Wars. Despite multiple expeditions, scientists cannot agree on what it is. Natural geological formation, or something far more unusual?",
                "footage_query": "ocean floor scanning sonar underwater exploration",
            },
            {
                "title": "The Yonaguni Monument",
                "narration": "Off the southern coast of Japan lies a massive underwater structure that has baffled researchers since its discovery in 1987. The Yonaguni Monument features perfectly flat platforms, right angles, and symmetrical steps carved into stone, all submerged at a depth of 25 meters. Some geologists insist these are natural rock formations shaped by ocean currents. But others point out the precision of the right angles and the complex layout as evidence of human construction, possibly dating back over 10,000 years to when sea levels were much lower.",
                "footage_query": "underwater ruins structure japan diving ancient",
            },
            {
                "title": "Underwater Brine Pools",
                "narration": "Deep beneath the Gulf of Mexico lies one of the ocean's most surreal features: underwater lakes and rivers. These brine pools are areas where super salty water collects on the ocean floor, creating a distinct boundary that looks exactly like a shoreline. The water is so dense that submarines can actually float on its surface. Any creature that swims into these toxic pools is quickly killed or sent into shock. Scientists are still studying how these formations develop and what role they play in deep ocean ecosystems.",
                "footage_query": "deep ocean floor strange underwater landscape brine",
            },
            {
                "title": "The Bermuda Triangle",
                "narration": "The Bermuda Triangle, stretching between Miami, Bermuda, and Puerto Rico, has been associated with the mysterious disappearance of ships and aircraft for over a century. Flight 19, a group of five Navy bombers, vanished during a training mission in 1945, and the rescue plane sent to find them also disappeared. Over the decades, more than 50 ships and 20 aircraft have been lost in this region. Theories range from rogue waves and methane eruptions to magnetic anomalies. Despite extensive investigation, no single explanation accounts for all the disappearances.",
                "footage_query": "ocean storm ships mysterious fog atlantic sea",
            },
            {
                "title": "The Mariana Trench",
                "narration": "At nearly 11 kilometers below the surface, the Mariana Trench is the deepest known point on Earth. The pressure at the bottom is over 1,000 times that at sea level, enough to crush most submarines. Yet life exists even here. Strange creatures like snailfish and amphipods thrive in total darkness under crushing pressure. In 2012, filmmaker James Cameron descended to the bottom in a solo dive, capturing footage of a landscape as alien as any on another planet. We have better maps of Mars than of our own ocean floor.",
                "footage_query": "deep ocean trench dark underwater abyss creatures",
            },
            {
                "title": "The Lost City of Dwarka",
                "narration": "According to Hindu scripture, Dwarka was a magnificent city built by Lord Krishna that sank into the sea after his death. For centuries, this was considered pure mythology. Then in 2001, marine archaeologists discovered an entire city submerged 40 meters beneath the waters of the Gulf of Khambhat off the coast of India. The ruins include walls, streets, and structures dating back an estimated 9,500 years, making it one of the oldest urban sites ever found. If confirmed, this discovery would rewrite our understanding of when human civilization began.",
                "footage_query": "submerged ancient city ruins underwater archaeology",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # SPACE MYSTERIES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "space": {
        "intro_hook": "The universe is unimaginably vast, and the more we explore it, the more we realize how little we actually understand. From unexplained signals arriving from deep space to invisible forces that shape the cosmos, these discoveries have left the world's greatest scientists searching for answers. These are the most mind-blowing mysteries of space.",
        "outro": "Space is full of things we cannot see, cannot explain, and can barely even detect. Every new discovery seems to raise ten new questions. Our universe is stranger than we ever imagined, and we have barely scratched the surface. If this video blew your mind, smash that like button and subscribe for more cosmic explorations. Which space mystery fascinates you the most? Drop it in the comments.",
        "items": [
            {
                "title": "The Wow Signal",
                "narration": "On August 15, 1977, astronomer Jerry Ehman was reviewing data from Ohio State University's Big Ear radio telescope when he spotted something extraordinary. A signal 30 times stronger than the background noise of deep space appeared for exactly 72 seconds. Ehman circled it on the printout and wrote Wow in red ink. The signal came from the direction of the constellation Sagittarius and has never repeated despite decades of monitoring. It matched the expected profile of an extraterrestrial communication. To this day, no natural or artificial explanation has been confirmed.",
                "footage_query": "radio telescope space observatory stars night sky",
            },
            {
                "title": "Dark Energy",
                "narration": "In 1998, two independent teams of astronomers made a discovery that shook the foundations of physics. The universe is not just expanding, it is accelerating. Something invisible and incredibly powerful is pushing galaxies apart at an ever increasing rate. Scientists named this force dark energy, but the truth is, we have no idea what it actually is. Dark energy makes up roughly 68 percent of the entire universe, yet it remains completely undetectable by any instrument. The most abundant thing in the cosmos is something we cannot see, touch, or explain.",
                "footage_query": "expanding universe galaxies cosmic dark space nebula",
            },
            {
                "title": "The Great Attractor",
                "narration": "Something enormous is pulling our entire region of the universe toward it at over 600 kilometers per second. Known as the Great Attractor, this gravitational anomaly lies roughly 250 million light years away in the direction of the Centaurus and Hydra constellations. The problem is, it sits directly behind the plane of our own Milky Way, making direct observation nearly impossible. Whatever it is, its gravitational influence affects hundreds of thousands of galaxies. Some astronomers believe it may be a massive supercluster, but we still cannot see it clearly enough to be certain.",
                "footage_query": "galaxy cluster cosmos deep space stars movement",
            },
            {
                "title": "Tabby's Star",
                "narration": "In 2015, astronomer Tabetha Boyajian identified a star 1,470 light years away that was doing something no other star had ever been observed doing. Its brightness would drop by up to 22 percent at irregular intervals. For comparison, a planet the size of Jupiter would only cause a 1 percent dip. The pattern was so unusual that some scientists seriously proposed a megastructure, a so called Dyson sphere, built by an advanced civilization to harvest the star's energy. While dust clouds are now the leading explanation, the true cause remains unconfirmed.",
                "footage_query": "bright star space dimming flickering cosmic light",
            },
            {
                "title": "Oumuamua",
                "narration": "In October 2017, astronomers detected the first known interstellar object passing through our solar system. Named Oumuamua, which means scout in Hawaiian, it had several unusual properties. Its shape was extremely elongated, like a cigar or pancake. It accelerated as it moved away from the Sun in a way that could not be explained by gravity alone. Harvard astronomer Avi Loeb controversially suggested it could be an alien light sail. Whether natural or artificial, Oumuamua left our solar system before we could study it further.",
                "footage_query": "asteroid space interstellar object cosmic deep space",
            },
            {
                "title": "Fast Radio Bursts",
                "narration": "First detected in 2007, Fast Radio Bursts are incredibly powerful blasts of radio energy from deep space that last only milliseconds. In that brief moment, they release more energy than our Sun does in 80 years. Most come from billions of light years away, making their source almost impossible to pinpoint. While some have been linked to magnetars, many bursts have no confirmed explanation. One repeating burst fires signals in a regular 157 day cycle. What is producing these signals across the cosmos remains one of astronomy's greatest puzzles.",
                "footage_query": "cosmic explosion radio waves space telescope stars",
            },
            {
                "title": "The Bootes Void",
                "narration": "In the northern sky lies a region of space so empty that it defies our understanding of the universe. The Bootes Void spans 330 million light years across and contains almost nothing. In a region where we would expect to find roughly 2,000 galaxies, astronomers have found only 60. It is the largest known void in the observable universe. Some scientists suggest it was formed by the merging of smaller voids over billions of years. Others question whether our models of cosmic structure are fundamentally incomplete. This vast emptiness raises more questions than answers.",
                "footage_query": "empty dark space void cosmic distant galaxies",
            },
        ],
    },

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # UNSOLVED MYSTERIES
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    "unsolved": {
        "intro_hook": "Some cases are so disturbing, so baffling, that even decades of investigation have failed to produce a single definitive answer. From bizarre deaths that defy explanation to coded messages that remain unbroken, these are real cases that investigators, scientists, and codebreakers have never been able to solve.",
        "outro": "These cases remain open. Despite advances in forensic science, DNA analysis, and digital investigation, the answers continue to elude us. Perhaps one day new evidence will surface, or new technology will crack what investigators could not. Until then, these mysteries endure. If this video gave you chills, hit like and subscribe for more deep dives into the unexplained. Which case do you think will be solved next? Let us know in the comments.",
        "items": [
            {
                "title": "The Dyatlov Pass Incident",
                "narration": "In February 1959, nine experienced hikers set out to cross the northern Ural Mountains in Russia. They never returned. Rescuers found their tent ripped open from the inside. The hikers had fled into minus 30 degree temperatures wearing almost nothing. Some were found with fractured skulls and broken ribs, yet there were no signs of a struggle. One was missing her tongue. Soviet investigators concluded they died from a compelling natural force and classified the case. Theories range from avalanche to military testing to infrasound panic. Over six decades later, no explanation accounts for all the evidence.",
                "footage_query": "snowy mountain wilderness winter mysterious tracks",
            },
            {
                "title": "The Somerton Man",
                "narration": "On December 1, 1948, the body of an unidentified man was found on Somerton Beach in Adelaide, Australia. He was well dressed, in good health, and had no identification. All labels had been removed from his clothing. In a hidden pocket, investigators found a scrap of paper with the words Tamam Shud, meaning ended or finished, torn from a rare copy of the Rubaiyat of Omar Khayyam. The book was later found with an encrypted message on its back cover that has never been decoded. Despite DNA analysis in 2022, the man's identity remains officially unresolved.",
                "footage_query": "beach mystery coastal city investigation old photograph",
            },
            {
                "title": "The Lead Masks Case",
                "narration": "On August 20, 1966, two electronic technicians were found dead on a hilltop in Niteroi, Brazil. They were wearing formal suits and crude lead eye masks, similar to those used as protection against radiation. Beside them lay a notebook with cryptic instructions about ingesting capsules at a specific time and then waiting for a signal. There were no signs of violence or poisoning. Witnesses reported seeing UFOs in the area that night. An autopsy was never performed. What the two men were doing on that hilltop and what killed them remains completely unexplained.",
                "footage_query": "hilltop night mystery investigation dark mysterious",
            },
            {
                "title": "The Hinterkaifeck Murders",
                "narration": "Six days before anyone noticed something was wrong, all six residents of the Hinterkaifeck farmstead in Bavaria, Germany were murdered with a mattock in 1922. The most disturbing detail is that the killer appeared to have remained on the farm for days afterward, feeding the livestock, eating food, and sleeping in the house. Footprints in the snow led to the farm but not away from it. The previous maid had quit weeks earlier, claiming the house was haunted. Over 100 suspects were investigated. No one was ever charged. The case remains open.",
                "footage_query": "old farmstead rural abandoned dark mysterious Europe",
            },
            {
                "title": "The SS Ourang Medan",
                "narration": "In June 1947, multiple ships in the Strait of Malacca received a distress signal from a Dutch cargo vessel called the SS Ourang Medan. The message read: All officers including captain are dead, lying in chartroom and bridge, possibly whole crew dead. Then a final chilling word: I die. When rescuers boarded the ship, they found the entire crew dead, their faces frozen in expressions of terror, arms outstretched. Before the ship could be towed to port, it exploded and sank. No cause of death was ever determined.",
                "footage_query": "ghost ship ocean fog mysterious abandoned vessel sea",
            },
            {
                "title": "The Taos Hum",
                "narration": "Since the early 1990s, residents of Taos, New Mexico have reported hearing a persistent low frequency humming sound that no one can identify or locate. Roughly 2 percent of the population can hear it, and they describe it as a constant drone similar to a distant diesel engine. Extensive testing with sensitive audio equipment has failed to detect any external source. The hum is also reported in locations around the world, including Bristol, England and Windsor, Ontario. Whether its origin is environmental, geological, or neurological remains unknown.",
                "footage_query": "desert landscape town quiet mysterious empty road",
            },
            {
                "title": "The Zodiac Cipher",
                "narration": "Between 1968 and 1969, a serial killer known as the Zodiac terrorized the San Francisco Bay Area, murdering at least five people. He sent taunting letters to newspapers, some containing complex cryptographic ciphers. While the first cipher was cracked within a week, the 340 character cipher remained unsolved for 51 years until 2020, when amateur codebreakers finally decoded it. But a third cipher, the Z13, containing the killer's real name, has never been solved. Despite one of the largest investigations in California history and DNA evidence, the Zodiac was never caught or identified.",
                "footage_query": "encrypted message code newspaper crime investigation",
            },
        ],
    },
}


# ── Script generation ────────────────────────────────────────────


def generate_script(topic, num_items=None):
    """Generate a complete video script with auto-detected niche."""
    print(f"Generating script for: {topic}")

    # Detect niche and count
    niche = detect_niche(topic)
    count = num_items or extract_count(topic)
    print(f"  Niche: {niche}")
    print(f"  Items: {count}")

    template = TEMPLATES[niche]
    items = template["items"][:count]

    # Build script
    script_lines = []
    scenes = []

    # ── Intro ──
    script_lines.append("[INTRO]")
    script_lines.append(template["intro_hook"])
    script_lines.append("")
    scenes.append({
        "scene_num": 0,
        "type": "intro",
        "title": "Introduction",
        "narration": template["intro_hook"],
        "footage_query": "mysterious dark cinematic atmosphere landscape",
        "duration_estimate": 15,
    })

    # ── Main items ──
    for i, item in enumerate(items):
        num = i + 1
        script_lines.append(f"[SECTION {num}: {item['title']}]")
        script_lines.append(item["narration"])
        script_lines.append("")
        scenes.append({
            "scene_num": num,
            "type": "section",
            "title": item["title"],
            "narration": item["narration"],
            "footage_query": item["footage_query"],
            "duration_estimate": 45,
        })

    # ── Outro ──
    script_lines.append("[OUTRO]")
    script_lines.append(template["outro"])
    scenes.append({
        "scene_num": len(items) + 1,
        "type": "outro",
        "title": "Outro",
        "narration": template["outro"],
        "footage_query": "cinematic landscape sunset mysterious atmospheric",
        "duration_estimate": 20,
    })

    full_script = "\n".join(script_lines)

    # Stats
    total_words = sum(len(s["narration"].split()) for s in scenes)
    est_min = total_words / 150

    # Save script text
    safe_topic = re.sub(r"[^\w\s-]", "", topic).strip().replace(" ", "_")[:50]
    script_path = os.path.join(SCRIPTS_DIR, f"{safe_topic}.txt")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"TOPIC: {topic}\n")
        f.write(f"NICHE: {niche}\n")
        f.write(f"ESTIMATED DURATION: {est_min:.1f} minutes\n")
        f.write(f"TOTAL WORDS: {total_words}\n")
        f.write(f"{'=' * 60}\n\n")
        f.write(full_script)

    # Save scenes JSON
    scenes_path = os.path.join(SCRIPTS_DIR, f"{safe_topic}_scenes.json")
    with open(scenes_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "topic": topic,
                "niche": niche,
                "scenes": scenes,
                "total_words": total_words,
                "est_duration_min": round(est_min, 1),
            },
            f,
            indent=2,
        )

    print(f"  Script saved: {script_path}")
    print(f"  Scenes saved: {scenes_path}")
    print(f"  Total words: {total_words}")
    print(f"  Estimated duration: {est_min:.1f} minutes")
    print(f"  Scenes: {len(scenes)}")

    return full_script, scenes, safe_topic


if __name__ == "__main__":
    # Test each niche
    generate_script("7 IMPOSSIBLE Ancient Discoveries We Still Can't Explain")
    print()
    generate_script("10 Scariest Ocean Discoveries")
    print()
    generate_script("5 Mind-Blowing Space Mysteries")
    print()
    generate_script("7 Unsolved Mysteries That Still Haunt Us")
