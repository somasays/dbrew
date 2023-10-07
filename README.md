# DBrew: Your Data Product Concoction Companion

Brew and orchestrate your data products seamlessly into actionable deployments with DBrew, the CLI tool tailored for modern data maestros.

## Features
- **YAML Configuration Validation:** Ensures your data product configurations are in check.
- **Automated Documentation Generation:** Keeps your project's documentation fresh and updated.
- **Docker Image Creation:** Preps your data for deployment with ease.
- **DAG Generation and Deployment:** Orchestrates your data workflows smoothly.

## Getting Started

### Prerequisites
- Ensure you have Docker installed.
- Have access to an Airflow instance for DAG deployment.

### Installation
```bash
pip install dbrew
```

### Usage
1. Navigate to the root of your data product project.
2. Create a dataproduct.yml file with your data product specifications.
3. Run the following command to validate your configuration, generate documentation, create a Docker image, and deploy your DAG:
```
dbrew brew
```

### Feedback
We value your feedback! For bug reports, feature requests, or general queries, feel free to open an issue.

### Contribute
Want to contribute to DBrew? We appreciate your help! Check out the CONTRIBUTING.md file for guidelines.

### License
DBrew is licensed under the MIT License. See the LICENSE file for details.
