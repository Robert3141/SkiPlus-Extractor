# SkiPlus-Extractor
Method of extracting Ski+ data into gpx format

## 1 - Get raw webpage with encoded data manually
- Login to [ski+](https://www.skiplus.fr/en/my-days/)
- On Firefox:
  - Launch Debugger in Firefox Developer Tools
  - Enable Event Listener load (from the sidebar)
  - Refresh the page
  - In Sources locate:
  ```
  Main Thread -> www.skiplus.fr -> en/mydays -> [SOME STRING OF NUMBERS].html
  ```
  - Save this html file

## 2 - Extract Webpage to gpx file
### TODO make as python script
- Extract relevant datapoints from file into pandas dataframe
- Save dataframe as gpx file
