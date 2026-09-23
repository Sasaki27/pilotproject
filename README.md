# pilotproject

# from the extracted portfolio-repo/ folder
cd portfolio-repo
git init
git add .
git commit -m "Ops analyst portfolio: SLA analysis, KPI scorecard, report automation"

# create the GitHub repo and push
gh repo create ops-analyst-portfolio --public --source=. --push
#   or without gh: create the repo on github.com, then
#   git remote add origin git@github.com:<username>/ops-analyst-portfolio.git && git push -u origin main
