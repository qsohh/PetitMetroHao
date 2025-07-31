# Railway Signal Simulator

This repository contains a simulation prototype of a railway signaling system, developed during my end-of-study internship (ENSTA Paris, 2019).

## Objectives
- Simulate train circulation under classical fixed-block and CBTC-based signaling signaling.
- Implement train dynamics and control logic (braking, coasting, station stop, etc.), with extensible architecture.
- Model tracks, nodes, junctions, balises, and terminus logic.
- Support multi-train scenarios with result visualization.

## Main Modules
- `DefClass/`: Core definitions (Train, Track, Station, Dummy logic...)
- `InitData/`: Scenario initialization files
- `PlotTool/`: Tools for data extraction and plotting
- `main.py`: Main execution file
- `test/`: Internal tests scripts

## Limitations
This project remains a exploratory prototype, only developed to support modeling during the internship. Several functions are incomplete, simplified, or hard-coded for testing purposes, but the architecture is modular and highly extensible.

## Example Output
- Position vs time plot
- Speed vs time plot
- Speed vs position plot
- Distance between trains

## Example usage
```bash
python main.py
```

## License
This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/) License.  
Commercial use is not permitted.