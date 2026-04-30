---
industry: [Physical AI, Robotics, Hospitality, Logistics]
scale: Scale-up (LG Subsidiary)
hq: Redwood City, CA
country: USA
tags: [PhysicalAI, SDR, Logistics, Hospitality, LG, PhysicalAIBody, company]
about: Silicon Valley-based leader in Physical AI and autonomous mobile robots (AMRs), now a subsidiary of LG Electronics.
---
> [!IMPORTANT] Key Takeaway (from my product & creative perspective)
> **Why this matters:** Bear Robotics represents the shift from "screen AI" to "Physical AI," where autonomous navigation meets high-frequency human service needs. Its acquisition by LG Electronics (2025) signifies a major consolidation in the service robot market, merging Bear's advanced software-defined robotics (SDR) with LG's hardware scale.
> **How to use it:** Monitor their transition from hospitality (Servi) to industrial/logistics (Carti/Cardi) as a blueprint for vertical expansion. Look for PM opportunities in "Physical AI" orchestration where multi-robot coordination (500+ units) is the next UX challenge.
> **Informs:** [[Edge-AI-Infrastructure-2026]], [[MakinaRocks]], and future Physical AI product strategies.

# Bear Robotics

Bear Robotics is a Silicon Valley-based leader in **Physical AI** and autonomous mobile robots (AMRs). Founded in 2017 by former Google engineer John Ha, the company has evolved from a hospitality-focused startup into a cornerstone of LG Electronics' robotics division.

## 🚀 Strategic Overview
- **LG Subsidiary:** In January 2025, LG Electronics acquired a 51% controlling stake in Bear Robotics. This move integrates LG’s "CLOi" line with Bear’s AI navigation platform to create a unified software-defined robotics (SDR) ecosystem.
- **Physical AI Vision:** Bear focuses on "moving AI into the physical world," automating repetitive tasks in hospitality, logistics, and cleaning to empower human workers.
- **Global Footprint:** Strong presence in the US, Korea, and Japan (Bear Robotics Japan LLC established in 2024).

## 🛠️ Product Portfolio

### 1. Hospitality (Servi Series)
- **Servi Plus:** High-capacity (88 lbs) delivery and bussing robot with advanced liquid-transport suspension (iF Design Award 2024).
- **Servi Lift:** Multi-floor robot capable of elevator navigation and secure deliveries in hotels/offices.
- **Servi Mini:** Agile robot for tight restaurant spaces.

### 2. Logistics & Industrial (Carti/Cardi Series)
- **Carti 100:** Modular AMR for warehouse transport (iF Design Award 2025).
- **Cardi 600 (New for 2026):** Mid-range industrial robot for cart lifting and pallet movement (600kg capacity).
- **Carti Low-Profile:** Heavy-duty powerhouse moving up to 1,500kg.
- **Carti Core:** An intelligent navigation platform for system integrators.

### 3. Cleaning
- **Servi Clean:** Autonomous floor-cleaning integrated into the "Bear Universe" fleet management system.

## 📅 Key Milestones (2024–2026)
- **2024:** $60M Series C led by LG Electronics; establishment of Japan operations.
- **2025:** LG completes majority acquisition (51%); shift toward software-defined robotics (SDR).
- **2026:** Debut of **Cardi 600** at MODEX; partnership with **FASSTO** for Physical AI logistics robots.

## ⚙️ Software-Defined Robotics (SDR) Architecture
A defining technical feature of Bear Robotics is its shift toward an **SDR paradigm**, which decouples robot intelligence from specific hardware.

### The Role of the `--model` Flag
In Bear’s unified software stack (Bear Universe/OS), the `--model` flag is the critical runtime parameter that tells the "brain" which "body" it is inhabiting.
- **Hardware Abstraction:** A single software image is deployed across the entire fleet. When a robot initializes (e.g., `./bear_os_core --model servi_plus`), the system loads the specific **Information Model** for that hardware.
- **Dynamic Configuration:** This flag triggers the loading of kinematic constraints, sensor maps, and actuator profiles unique to that model (Servi, Carti, or custom LG hardware).
- **PM Insight:** For a 0→1 PM, this architecture is a massive "force multiplier." It allows for rapid prototyping of new hardware forms without rewriting core navigation or AI logic, effectively creating an "Android for Robots" ecosystem.

## 🔗 Connections
- [[Edge-AI-Infrastructure-2026]] - Hardware/Software stack for on-device navigation.
- [[MakinaRocks]] - Synergies in industrial AI and predictive maintenance.
- [[AI-Startups-Korea-2026]] - Bear is a key player in the Korea-originated global robot landscape.
- [[Superb-AI]] - Potential for vision AI training in complex physical environments.
