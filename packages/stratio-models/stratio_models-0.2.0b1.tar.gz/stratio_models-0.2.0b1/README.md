# Stratio Models

This repository contains shared models for AWS Marketplace.

## Overview

The package provides Pydantic models for:
- Clusters (e.g., `ClusterItem`, `ClusterMetadataItem`, `ClusterTableData`)
- AWS resources (e.g., `EC2Item`, `EKSItem`)
- Customers (e.g., `CustomerItem`, `CustomerTableData`)
- Logs (e.g., `StreamItem`)
- Repositories (e.g., `Chart`, `UploadResult`)

These models enforce data validation and consistency across applications using AWS Marketplace data.

## Installation

Ensure you are using:
- Python \>= 3.12, \< 4.0
- Pydantic == 2.10.3

This project uses Poetry for dependency management. To install dependencies, run:

```bash
poetry install