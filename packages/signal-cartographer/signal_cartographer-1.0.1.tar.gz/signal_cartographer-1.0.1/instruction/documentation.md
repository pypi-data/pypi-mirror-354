## Game Design Document: The Signal Cartographer: Echoes from the Void

**Version:** 1.0
**Prepared for:** You! (For TerminalCraft Submission)
**Date:** May 27, 2025

### File Structure
The Signal Cartographer/
├── README.md
├── requirements.txt
├── main.py                          # Entry point
├── run.sh                          # Linux launcher script
├── run.bat                         # Windows launcher script
│
├── src/                            # Core game code
│   ├── __init__.py
│   ├── game_core.py               # Main game controller
│   ├── aethertap.py               # Terminal interface manager
│   ├── signal_system.py           # Signal detection/management
│   ├── command_parser.py          # CLI command processing
│   ├── progression.py             # Upgrades & tech tree
│   ├── map_system.py              # Star map & navigation
│   ├── save_system.py             # Game state persistence
│   │
│   ├── ui/                        # User interface components
│   │   ├── __init__.py
│   │   ├── panes.py              # Individual pane managers
│   │   ├── layout.py             # Screen layout & positioning
│   │   ├── colors.py             # Color schemes & themes
│   │   └── input_handler.py      # Keyboard input processing
│   │
│   ├── puzzles/                   # Decoding mini-games
│   │   ├── __init__.py
│   │   ├── base_puzzle.py        # Abstract puzzle class
│   │   ├── pattern_matching.py   # Visual pattern puzzles
│   │   ├── crypto_puzzles.py     # Caesar, Vigenère, etc.
│   │   ├── logic_puzzles.py      # Circuit completion, sequences
│   │   ├── audio_patterns.py     # Morse code, rhythm patterns
│   │   └── puzzle_factory.py     # Puzzle selection logic
│   │
│   ├── content/                   # Content management
│   │   ├── __init__.py
│   │   ├── signal_generator.py   # Signal creation & selection
│   │   ├── lore_manager.py       # Story content handling
│   │   ├── ascii_library.py      # ASCII art management
│   │   └── story_arcs.py         # Narrative thread tracking
│   │
│   └── utils/                     # Utility functions
│       ├── __init__.py
│       ├── file_manager.py       # File I/O operations
│       ├── text_utils.py         # Text formatting & wrapping
│       ├── ascii_tools.py        # ASCII manipulation
│       └── crypto_utils.py       # Encryption/decryption helpers
│
├── data/                          # Game data files
│   ├── signals/                   # Signal definitions
│   │   ├── signals.json          # Main signal database
│   │   ├── story_arc_1.json      # Ancient Beacon arc
│   │   ├── story_arc_2.json      # Wandering Ship arc
│   │   ├── story_arc_3.json      # Quantum Echoes arc
│   │   └── random_signals.json   # Standalone signals
│   │
│   ├── ascii_art/                # ASCII art library
│   │   ├── signatures/           # Signal visual signatures
│   │   │   ├── ancient_beacon.txt
│   │   │   ├── quantum_pulse.txt
│   │   │   ├── bio_signal.txt
│   │   │   └── ...
│   │   ├── schematics/           # Upgrade schematics
│   │   │   ├── noise_filter.txt
│   │   │   ├── quantum_decoder.txt
│   │   │   └── ...
│   │   ├── maps/                 # Star map elements
│   │   │   ├── sector_alpha.txt
│   │   │   ├── anomaly_01.txt
│   │   │   └── ...
│   │   └── ui_elements/          # Interface decorations
│   │       ├── borders.txt
│   │       ├── logos.txt
│   │       └── ...
│   │
│   ├── lore/                     # Story content
│   │   ├── fragments/            # Individual lore pieces
│   │   │   ├── ancient_01.txt
│   │   │   ├── scientist_log_03.txt
│   │   │   └── ...
│   │   ├── story_arcs/           # Connected narratives
│   │   │   ├── beacon_mystery.txt
│   │   │   └── ...
│   │   └── lore_index.json       # Lore organization
│   │
│   ├── upgrades/                 # Tech tree data
│   │   ├── upgrades.json         # All available upgrades
│   │   ├── tech_tree.json        # Dependency relationships
│   │   └── costs.json            # Resource requirements
│   │
│   ├── maps/                     # Star map data
│   │   ├── sectors.json          # Sector definitions
│   │   ├── coordinates.json      # Known locations
│   │   └── navigation.json       # Travel requirements
│   │
│   └── config/                   # Configuration files
│       ├── game_config.json      # Core game settings
│       ├── ui_config.json        # Interface preferences
│       ├── commands.json         # Command definitions
│       └── keybindings.json      # Input mappings
│
├── saves/                        # Player save files
│   ├── .gitkeep                  # Keep directory in git
│   └── [player_saves.json]       # Generated at runtime
│
├── assets/                       # Additional resources
│   ├── docs/                     # Documentation
│   │   ├── player_manual.md
│   │   ├── command_reference.md
│   │   └── lore_compendium.md
│   ├── tools/                    # Development utilities
│   │   ├── ascii_generator.py    # ASCII art creation helper
│   │   ├── signal_validator.py   # Data validation
│   │   └── content_builder.py    # Content management tool
│   └── examples/                 # Sample content
│       ├── sample_signals.json
│       └── sample_ascii.txt
│
├── tests/                        # Unit tests
│   ├── __init__.py
│   ├── test_signal_system.py
│   ├── test_puzzles.py
│   ├── test_command_parser.py
│   ├── test_ui_components.py
│   └── test_game_flow.py
│
├── instruction/                  # Project documentation
│   ├── documentation.md          # Current comprehensive doc
│   ├── development_log.md        # Progress tracking
│   └── terminalcraft_submission.md
│
└── logs/                         # Runtime logs
    ├── .gitkeep
    └── [debug.log]               # Generated at runtime


## Game Design Document: The Signal Cartographer: Echoes from the Void

**Version:** 1.1
**Prepared for:** You! (For TerminalCraft Submission)
**Date:** May 28, 2025

---

> **Note:** As of version 1.1, we are officially **replacing the use of the `curses` library** due to glitches, limitations, and complexity in cross-platform handling. We are switching to **[`textual`](https://github.com/Textualize/textual)** — a modern, async-friendly Python library for building rich TUI (Text-based User Interfaces). This update enhances UI stability, improves development workflow, and allows more expressive, maintainable layouts. `textual` is now the core library for all interface components.

---


### 1. Game Overview

* **Title:** The Signal Cartographer: Echoes from the Void
* **Genre:** Sci-Fi Mystery, Exploration, Puzzle, Text-Based Adventure (with rich ASCII art).
* **Target Audience:** TerminalCraft judges and participants; players who enjoy mystery, discovery, code-breaking, and atmospheric, text-driven experiences.
* **Core Concept:** The player is a Signal Cartographer who uses a terminal-based rig to detect, decode, and map mysterious signals from deep space, uncovering lore and upgrading their equipment.
* **Unique Selling Points (USPs):**
    * **Deeply Integrated ASCII Art:** Visuals are not just decorative but central to gameplay (analyzing signal patterns, navigating maps, viewing schematics).
    * **Original Premise & Lore:** A unique universe built from scratch by you.
    * **Intellectual Challenge:** Engaging puzzle mechanics for signal decoding.
    * **Atmospheric Immersion:** Creates a strong sense of mystery and exploration within the terminal.
    * **Dual Mode Potential:** A robust, self-contained Classic Mode, with an optional AI-enhanced Dynamic Mode for richer, unpredictable elements.

### 2. Story & Setting

* **The Premise:** In a future where interstellar travel is nascent or limited, the cosmos hums with an orchestra of strange signals. These "Echoes" are poorly understood – some may be natural phenomena, others the remnants of long-dead civilizations, active communications from unknown entities, or even dangerous memetic hazards.
* **Player Role:** An independent, curious, and resourceful Signal Cartographer operating from a modest, self-built rig (the "AetherTap"). Driven by a thirst for knowledge, the thrill of discovery, or perhaps a personal mystery, the player ventures into the uncharted frequencies of space.
* **The Mystery:** What are these signals? Who (or what) sent them? What do they mean for humanity or the universe? The game unfolds these mysteries gradually through the lore snippets decoded from the signals. There might be overarching narrative threads connecting different signals or pointing towards a larger cosmic event or entity.
* **Tone:** Mysterious, atmospheric, slightly melancholic, with moments of awe, wonder, and perhaps a touch of cosmic dread.

### 3. Gameplay Mechanics (Classic Mode)

This is the core, self-contained game for TerminalCraft.

#### 3.1. The AetherTap - Your Terminal Rig Interface

The game is played entirely through this ASCII interface.

* **Main Spectrum Analyzer (`[MSA]` Pane):**
    * **Function:** Real-time display of signal activity across a selected frequency band. Signals appear as dynamic ASCII patterns (lines, blocks, symbols) differentiated by character choice, density, color (if supported), and animation (e.g., pulsing, drifting). Noise is a faint, shifting background.
    * **Interaction:** Primarily visual. Player observes for anomalies and interesting patterns.
* **Signal Focus & Data (`[SFD]` Pane):**
    * **Function:** Displays detailed information about a single, isolated signal. Shows its unique pre-generated ASCII "signature" (a complex visual identifier), properties like frequency, strength, apparent origin (if known), modulation type (e.g., AM, FM, Pulsed, Phase-Shifted - represented textually or symbolically), and stability.
    * **Interaction:** View data, select focused signal for analysis.
* **Cartography & Navigation (`[CNP]` Pane):**
    * **Function:** Displays an ASCII star map. Initially sparse, it fills in as the player explores and plots signal origins. Can show sectors, star systems, known anomalies, and confirmed signal sources. Supports zooming/panning via commands.
    * **Interaction:** `Maps TO <SECTOR_COORDS>`, `PLOT_SOURCE <SIGNAL_ID> AT <COORDS>`, `ZOOM_MAP <LEVEL>`.
* **Decoder & Analysis Toolkit (`[DAT]` Pane):**
    * **Function:** The interactive workspace for decoding. Its appearance changes based on the active tool or puzzle.
    * **Interaction:** Input commands, select options, manipulate ASCII elements to solve puzzles.
* **Captain's Log & Database (`[CLD]` Pane):**
    * **Function:** Automatically records important information: decoded lore entries, signal parameters, discovered coordinates, schematics, active missions/goals (if any). Can be searched.
    * **Interaction:** `LOG_SEARCH <KEYWORD>`, `VIEW_ENTRY <ID>`.
* **Command Line Interface (`[CLI]`):**
    * **Function:** Primary input method. Supports a specific command syntax.
    * **Interaction:** Player types commands like `SCAN`, `FOCUS`, `ANALYZE`, `UPGRADE`, etc. Autocompletion/suggestions would be a great advanced feature.

#### 3.2. Scanning & Signal Detection

* Player initiates a scan of a chosen frequency band or spatial sector (`SCAN SECTOR DELTA-9 FREQ_RANGE 100-150MHZ`).
* The `[MSA]` pane updates, showing signals as ASCII patterns. Fainter or more distant signals might have less distinct patterns or flicker.
* Your algorithm determines which signals appear based on player location, scanner sensitivity, and pre-defined "signal events" or densities in different regions.

#### 3.3. Signal Characteristics

Each signal has parameters that influence its appearance and decoding:
* **Frequency:** Where it appears on the `[MSA]`.
* **Strength:** Affects visibility and how easily it can be "locked onto."
* **Stability:** How much it drifts or fluctuates; unstable signals might be harder to decode.
* **Modulation Type:** A textual tag (e.g., "Pulsed-Echo," "Phase-Ciphered," "Bio-Luminescent Ripple") that hints at the required decoding method or tool.
* **Visual Signature:** A unique, complex pre-generated ASCII pattern displayed in the `[SFD]` when focused. This is a key visual identifier.
* **Tier/Complexity:** An internal value determining puzzle difficulty and reward quality.

#### 3.4. Filtering & Isolation

* Player selects a promising signal from the `[MSA]` (e.g., `FOCUS SIGNAL_MSA_3`).
* Commands like `APPLY_FILTER NOISE_REDUCTION_HIGH` or `TUNE_FREQUENCY <value> SHARPNESS <value>` can clarify the signal in the `[SFD]` or stabilize it. Success might be indicated by a clearer ASCII signature or improved stats.

#### 3.5. Decoding Puzzles & Mini-Games

This is the core challenge. A signal might require multiple stages or types of decoding.

* **Visual Pattern Matching:**
    * The signal's ASCII signature in `[SFD]` contains a hidden pattern or needs to be matched against a "key" pattern from your library (which could be an upgradeable tool).
    * Example: An ASCII "constellation" within the signature must be identified.
* **Linguistic Cryptography:**
    * For text-based signals. Tools could include:
        * `CAESAR_DECRYPT <shift_value>`
        * `VIGENERE_DECRYPT <key_word>` (keyword might be found from other signals/lore)
        * `SYMBOL_SUBSTITUTION <symbol_map_file>`
        * `FREQUENCY_ANALYSIS` (displays character counts to aid manual decryption).
* **Logic Puzzles (ASCII-based):**
    * **Mastermind / Bulls & Cows:** Guess a sequence of symbols/colors.
    * **Circuit Completion:** Connect nodes in an ASCII grid to complete a circuit.
    * **Sequence Deduction:** Identify the next element in a complex ASCII pattern sequence.
    * **Rule Inference:** Observe input/output transformations on ASCII strings and deduce the hidden rule.
* **Audio Pattern Interpretation (Textual):**
    * Since it's terminal, "audio" patterns are represented textually (e.g., "LONG_PULSE SHORT_PULSE SHORT_PULSE LONG_SILENCE..."). Player might need to translate this into Morse code or another symbolic language.
* **Resource-Gated Decoding:** Some high-tier signals might require spending "Decryption Cycles" (an expendable resource earned from simpler signals or found) to attempt a solution.

Successful decoding yields Lore, Schematics, Coordinates, or Resources. The `[DAT]` pane would show the raw decoded output (which could be more ASCII art).

#### 3.6. Mapping & Navigation

* Decoded coordinates are plotted on the `[CNP]` star map.
* This might reveal new explorable sectors, specific star systems, anomalies, or the path of a signal "chain."
* Navigation to new sectors might require specific drive upgrades or consume "Fuel" (another potential resource).

#### 3.7. Resource Management (Optional, but adds depth)

* **Decryption Cycles:** Earned or found, spent on complex decoding attempts.
* **Fuel/Energy:** For rig operation, scanning, or interstellar travel on the map.
* **Scrap/Components:** Salvaged from certain signals or locations, used for upgrades.

#### 3.8. Progression & Upgrades (Tech Tree)

Decoded schematics unlock upgrades for the AetherTap. Player spends resources to craft them.
* **Scanner:** Increased range, sensitivity (detect fainter signals), wider frequency bands.
* **Filters:** Better noise reduction, signal stabilization.
* **Decoder Modules:** New puzzle types/tools (e.g., "Quantum Entanglement Solver," "Heuristic Cipher Breaker MkII").
* **Cartography Suite:** Faster map updates, anomaly prediction.
* **Database:** Increased storage for lore, faster search.
* **Rig Efficiency:** Reduced fuel/energy consumption.

#### 3.9. Lore Discovery & Narrative Unfolding

* Decoded signals provide text snippets (lore).
* These snippets might be fragmented diary entries, scientific observations, poetry, warnings, historical records, philosophical texts, etc., from unknown origins.
* Over time, players piece together stories, learn about ancient civilizations, cosmic phenomena, or recurring entities. Some signals might form a "chain" or "story arc."

#### 3.10. Example Signal Flow

1.  Player `SCANS` a sector. `[MSA]` shows several signals.
2.  Player `FOCUSES` on `SIG_001` (a complex, pulsing ASCII pattern). `[SFD]` shows its stats and unique visual signature. Modulation: "Fragmented Echo."
3.  Player tries `ANALYZE SIG_001 TOOL=SPECTRAL_RECONSTRUCTION`. `[DAT]` pane shows a mini-game where they must align ASCII "fragments" to form a coherent image.
4.  Success! The image is an ASCII schematic for a "Basic Noise Filter." Lore unlocked: "Fragment 7: ...stars bleed static..."
5.  Player uses `UPGRADE INSTALL BASIC_NOISE_FILTER`.
6.  Player `SCANS` again. A previously hidden, fainter signal `SIG_002` is now visible thanks to the filter. Its signature in `[SFD]` looks like encrypted text. Modulation: "Ciphered Stream."
7.  Player uses `ANALYZE SIG_002 TOOL=FREQUENCY_ANALYSIS`. `[DAT]` shows letter counts. Player deduces a Caesar cipher, uses `CAESAR_DECRYPT SIG_002 SHIFT=5`.
8.  Success! Decoded text: "Coordinates: Sector Gamma-7, Object XJ-100. Warning: High energy readings." Lore: "Log Entry 23: The entity at XJ-100 pulses with an unknown energy. We dare not approach closer."
9.  Player uses `PLOT_SOURCE SIG_002 AT GAMMA-7/XJ-100` on the `[CNP]` map. A new marker appears.

### 4. ASCII Art Integration Strategy

* **Pre-Generated Library:** This is key for Classic Mode.
    * You (the developer) will create a large collection of ASCII art using various tools:
        * Manual creation for specific UI elements and key symbols.
        * AI art generators (e.g., from images, or text-to-ASCII tools) to produce a vast number of diverse signal signatures, alien schematics, "found art" from signals, environmental details for maps, etc.
        * Image-to-ASCII converters (`jp2a`, online tools) for specific imagery.
        * Python libraries like Pillow could be used to script generation of simpler patterns or glyphs.
* **Algorithmic Selection & Presentation:**
    * The game's code will contain logic to select appropriate ASCII art from this library based on context:
        * Signal type, strength, frequency, and location could map to specific subsets of visual signatures.
        * Progression in a story arc might unlock specific ASCII images as decoded lore.
        * Random selection (from appropriate pools) can provide variety for generic signals or background details.
    * This makes the world feel rich and varied without runtime AI. ASCII art is stored as text files or strings within your code/data files.
* **Dynamic ASCII (in Classic Mode):** The `[MSA]` spectrum display is dynamic, generated by your algorithms using basic characters to represent signal strength and noise over time. Simple animations (pulsing, flickering) can be achieved by redrawing parts of the screen with slight variations.

### 5. Dynamic (AI) Mode - Optional Enhancements

(Clearly marked as optional, possibly requiring user setup like an API key).
* **Enhanced Text Generation:** For specific, rare signals, an LLM could generate more nuanced, poetic, or truly alien-feeling textual content (dialogue, lore, descriptions) beyond the pre-scripted classic mode data.
* **Reactive Signals:** Some unique signal sources could use an LLM to generate more dynamic, conversational responses if the player tries to "communicate" (e.g., sending back a simple pattern).
* **Emergent Lore & Hypotheses:** An LLM could analyze the player's collection of decoded lore and generate speculative summaries or new "research threads" in their journal, personalizing the narrative.
* **Atmospheric "Ghost" Events:** LLM generates fleeting, unexplainable textual or visual phenomena within the AetherTap interface – strange error messages, cryptic whispers in the static, visual glitches – adding to the mystery and sense of an active, unpredictable universe. (These should not break core gameplay).

### 6. Technical Considerations

* **Language:** **Python 3.**
* **Core Libraries (Python Standard Library):**

  * **`sqlite3`:** For storing game state, player progress, discovered lore, the signal database (if it becomes large and complex), and the mapping of pre-generated ASCII art to game elements.
  * **`json`:** For simpler data storage (e.g., configuration files, individual signal definitions if not using SQLite).
  * **`random`:** For procedural generation aspects, selecting random signals/events.
  * **`textwrap`:** For formatting text neatly within panes.
* **New Core UI Library (External):**

  * **`textual`:** Replacing `curses`. Provides pane layout, keyboard input, async updates, and ASCII rendering in a structured and modern way. Ideal for handling the AetherTap interface across platforms.

    * Install with: `pip install textual`
    * Used in `src/ui/` for all components (`layout.py`, `panes.py`, `input_handler.py`, `colors.py`).
* **Optional Libraries:**

  * **`prompt_toolkit`:** Could be explored for command-line autocompletion or input enhancements.
  * **`numpy`:** For complex signal pattern generation or analysis (use only if justified).
* **Developer ASCII Art Tools (Not part of the game runtime):**

  * Any text editor.
  * Online ASCII art generators.
  * Command-line tools like `jp2a` (Linux).
  * Image editing software to create source images for conversion.
* **Data Management:**

  * Game data (signal definitions, lore entries, ASCII art strings/filepaths) can be stored in JSON files, Python dictionaries, or an SQLite database. SQLite is robust for larger amounts of structured data.
* **Linux Compatibility:**

  * Python and its standard libraries are inherently cross-platform. `textual` also supports Linux, Windows, and macOS. Provide clear install/run instructions. Avoid complex binary packaging if possible — self-contained scripts are preferred for ease of submission.

* **Data Management:**
    * Game data (signal definitions, lore entries, ASCII art strings/filepaths) can be stored in JSON files, Python dictionaries, or an SQLite database. SQLite is robust for larger amounts of structured data.
* **Linux Compatibility:** Python and its standard libraries are inherently cross-platform. `curses` is standard on Linux. Ensure any external libraries are also Linux-compatible. Provide pre-built binaries (e.g., using PyInstaller if necessary, though for TerminalCraft, providing the Python scripts and clear run instructions might be preferred if dependencies are minimal). *Self-contained scripts are often better than relying on users to install complex binaries.*

### 7. Game Scope & Scalability (For TerminalCraft)

* **Minimum Viable Product (MVP) for TerminalCraft:**
    * Functional AetherTap interface (at least `[MSA]`, `[SFD]`, `[CLI]`, and basic `[CLD]`).
    * Core loop: Scan -> Detect basic signals -> Isolate -> One or two simple decoding puzzle types (e.g., pattern matching, simple cipher).
    * A small, curated set of pre-generated ASCII art for signals and decoded lore.
    * Basic progression: Decode a few signals to get a snippet of a story or a simple "win" message.
    * Focus on making the core loop engaging and showcasing the originality.
* **Scalability:**
    * Add more signal types and complexity.
    * Introduce more decoding mini-games/puzzles.
    * Expand the library of ASCII art.
    * Develop a more complex tech tree for upgrades.
    * Create deeper narrative arcs and lore.
    * Flesh out the star map with more regions.
    * Add resource management systems.

### 8. Stretch Goals / Future Ideas (Beyond TerminalCraft)

* More sophisticated AI integration in Dynamic Mode.
* Procedurally generated ASCII art at runtime (challenging but cool).
* Player-to-player signal sharing (e.g., sharing codes for particularly interesting procedural signals).
* Deeper economic simulation if trading discovered data/tech.
* Actual sound integration (if ever moving beyond pure terminal).
