scrapy crawl freebuf -s JOBDIR=jobs/job-1

echo "[*] generating freebuf.html..."
python generate_html.py

echo "[+] finished"