from selenium import webdriver
import csv
import env

iterations = 50
csv_path = f"/data/headless_run{iterations}.csv"
hyperlink = env.host


op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)

try:
    file = open(csv_path, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(["backendPerformance_calc","frontendPerformance_calc"])

    for i in range(iterations):
        driver.get(hyperlink)

        # Use Navigation Timing API to calculate the timings
        navigationStart = driver.execute_script("return window.performance.timing.navigationStart")
        responseStart = driver.execute_script("return window.performance.timing.responseStart")
        domComplete = driver.execute_script("return window.performance.timing.domComplete")

        backendPerformance_calc = responseStart - navigationStart
        frontendPerformance_calc = domComplete - responseStart
        writer.writerow([backendPerformance_calc, frontendPerformance_calc])

        print(f"start next iteration {i+1}")
except:
    print("error opening or writing to the CSV file!")
finally:
    driver.close()
    file.close()








