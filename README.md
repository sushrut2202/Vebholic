# Vebholic

# Generator Data Automation

This repository contains a Python-based automation script for gathering and validating ownership information about energy generation projects. The primary goal is to research each generator (project) in an assigned list to find the company that owns it using various methods, including web scraping and parsing interconnection studies.

### **Project Overview**

The script performs the following tasks:
1. **Web Scraping**: Scrapes publicly available data for project details like fuel type, capacity, status, location, and transmission owner.
2. **Data Validation**: Compares scraped data with the provided dataset to ensure the accuracy of project information.
3. **Queue ID Research**: Uses Queue ID to find supporting interconnection documents and agreements containing ownership details.
4. **Filling Out Ownership Data**: Adds the gathered ownership information and source URLs to the dataset.
