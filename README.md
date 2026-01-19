Neonatal Incubator IoT Thermal Monitoring (Mission-Critical OT)

Project Overview
This project is an advanced data acquisition system designed for the continuous monitoring of thermal environments in neonatal incubators. 
Given the fragility of the patients, the system prioritizes data integrity and real-time precision, strictly following the IEC 60601-2-19:2020 
international standard for medical electrical equipment safety and essential performance.

Project Status: Metrological Prototype & Compliance Analysis
This system is a Functional Prototype designed to validate the end-to-end data pipeline. Based on a professional metrological assessment, the following gap has been identified:
    • Standard Requirement (IEC 60601-2-19:2020): Demands a measurement precision better than 0.5°C for essential performance and safety.
    • Current Hardware Limitation: The DS18B20 digital sensor utilized in this version provides a precision of ± 0.5°C.
    • Engineering Conclusion: While this hardware is optimal for logic prototyping and AI-assisted workflow testing, it does not meet the final clinical requirements for "essential performance."
    • Roadmap: Future iterations involve replacing the DS18B20 with high-precision medical-grade thermistors or RTDs to achieve the required accuracy.
Functional Analysis: 6-Node Thermal Mapping
While this version is a metrological prototype, it excels as a Diagnostic & Mapping Tool.
    • Spatial Fidelity: The system utilizes 6 sensors distributed across the incubator's enclosure. This allows for a high-fidelity reproduction of the internal thermal environment.
    • Operational Insights: The multi-sensor array is highly effective for identifying air circulation patterns, heat loss zones, and stabilization times, providing a comprehensive "thermal map" of the unit.
    • Software Validation: This prototype successfully validates the software architecture and data ingestion pipeline, demonstrating that the logic is ready for higher-precision hardware.

Technical Architecture (IT/OT Convergence)
The pipeline is structured to ensure zero data loss from the physical environment to the analytical layer:

1. Sensing Layer: Utilizes high-precision DS18B20 digital sensors via the OneWire protocol to achieve a resolution of 0.5°C, ensuring compliance with clinical safety thresholds.
2. Firmware (Arduino): Implements asynchronous routines on an Arduino Nano to handle sensor polling without blocking the communication cycle.
3. Ingestion Layer (Python): A custom pipeline that manages serial communication, performs real-time data validation, and logs structured data for clinical audit trails.
  
Development Methodology: AI-Assisted Architecture
Following a Human-in-the-Loop (HITL) framework, I acted as the primary technical architect to orchestrate LLMs in generating robust, fault-tolerant code.

Key Milestones reached via Iterative Feedback:
* Fault Tolerance: Implemented exception handling for serial disconnects, ensuring the system recovers automatically without losing historical data.
* Signal Optimization: Refined the logic through "n" iterations to filter electronic noise and sensor spikes, ensuring "AI-ready" data quality.

Tech Stack
* Languages: Python, C++ (Arduino)
* Hardware: DS18B20 Sensors, Arduino Nano
* Compliance: Aligned with IEC 60601-2-19 safety requirements for infant incubators.
