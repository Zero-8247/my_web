from flask import Flask, render_template_string
import json

app = Flask(__name__)

# ── 球队数据（你可以直接在这里修改内容）──────────────────────────
TEAM_NAME = "卢一足球校队"
TEAM_SLOGAN = "团结·拼搏·荣耀"
TEAM_INTRO = "卢一足球校队成立于2015年，代表学校参加市级及区级各类足球赛事。我们相信足球不只是运动，更是培养团队精神与拼搏意志的舞台。"

MEMBERS = [
    {"name": "张伟", "number": 1,  "position": "守门员", "grade": "高三", "goals": 0,  "assists": 2},
    {"name": "李明", "number": 5,  "position": "中后卫", "grade": "高二", "goals": 2,  "assists": 1},
    {"name": "王磊", "number": 8,  "position": "中场核心", "grade": "高三", "goals": 7,  "assists": 9},
    {"name": "陈浩", "number": 10, "position": "前锋",   "grade": "高二", "goals": 12, "assists": 5},
    {"name": "刘阳", "number": 11, "position": "左边锋", "grade": "高一", "goals": 8,  "assists": 6},
    {"name": "赵强", "number": 4,  "position": "右后卫", "grade": "高二", "goals": 1,  "assists": 4},
]

MATCHES = [
    {"date": "2025-03-15", "opponent": "二中足球队", "home": True,  "score": "3-1", "status": "胜"},
    {"date": "2025-03-22", "opponent": "三中足球队", "home": False, "score": "2-2", "status": "平"},
    {"date": "2025-04-05", "opponent": "四中足球队", "home": True,  "score": "1-0", "status": "胜"},
    {"date": "2025-04-19", "opponent": "五中足球队", "home": False, "score": "0-2", "status": "负"},
    {"date": "2025-05-10", "opponent": "市联赛半决赛", "home": True, "score": "—",  "status": "即将"},
    {"date": "2025-05-24", "opponent": "市联赛决赛",   "home": True, "score": "—",  "status": "即将"},
]

NEWS = [
    {"date": "2025-04-06", "title": "卢一足球队以1-0险胜四中，晋级半决赛！", "summary": "昨日主场，队长王磊在下半场第72分钟打入制胜球，全队奋勇拼搏，成功晋级市联赛半决赛。"},
    {"date": "2025-03-23", "title": "客场平局，积分榜稳居前三", "summary": "在三中客场的比赛中，双方各进两球，我队凭借顽强意志平局收场，积分榜排名稳居前三。"},
    {"date": "2025-03-10", "title": "新赛季训练正式开始，全队士气高昂", "summary": "新赛季集训正式启动，全队26名球员参与，教练组制定了详细的训练计划，备战市级联赛。"},
]
# ──────────────────────────────────────────────────────────────────

HTML = """
<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ team_name }} — 官方网站</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
:root {
  --blue:    #00c3ff;
  --blue2:   #0077ff;
  --dark:    #030b18;
  --dark2:   #071428;
  --card:    #0a1f3a;
  --border:  rgba(0,195,255,0.18);
  --text:    #cce6ff;
  --muted:   #5a8ab0;
  --win:     #00e676;
  --draw:    #ffca28;
  --loss:    #ff5252;
  --soon:    #00c3ff;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: 'Noto Sans SC', sans-serif;
  background: var(--dark);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Grid bg ── */
body::before {
  content: '';
  position: fixed; inset: 0;
  background-image:
    linear-gradient(rgba(0,195,255,0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0,195,255,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  pointer-events: none;
  z-index: 0;
}

/* ── NAV ── */
nav {
  position: fixed; top: 0; left: 0; right: 0; z-index: 100;
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 5%;
  height: 64px;
  background: rgba(3,11,24,0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.nav-logo {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem; font-weight: 900;
  color: var(--blue);
  letter-spacing: 2px;
  text-decoration: none;
}
.nav-links { display: flex; gap: 2rem; list-style: none; }
.nav-links a {
  color: var(--muted); font-size: .85rem; letter-spacing: 1px;
  text-decoration: none; text-transform: uppercase;
  transition: color .2s;
}
.nav-links a:hover { color: var(--blue); }

/* ── HERO ── */
#hero {
  position: relative; z-index: 1;
  min-height: 100vh;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  text-align: center;
  padding: 0 5%;
  overflow: hidden;
}
.hero-glow {
  position: absolute;
  width: 600px; height: 600px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(0,119,255,0.18) 0%, transparent 70%);
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}
.hero-badge {
  display: inline-block;
  border: 1px solid var(--border);
  background: rgba(0,195,255,0.07);
  color: var(--blue);
  font-size: .75rem; letter-spacing: 3px;
  text-transform: uppercase;
  padding: .4rem 1.2rem;
  border-radius: 99px;
  margin-bottom: 1.5rem;
  animation: fadeUp .8s ease both;
}
h1.hero-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(2.4rem, 7vw, 5rem);
  font-weight: 900;
  line-height: 1.1;
  color: #fff;
  animation: fadeUp .8s .15s ease both;
}
h1.hero-title span { color: var(--blue); }
.hero-slogan {
  margin-top: 1rem;
  font-size: 1rem; color: var(--muted); letter-spacing: 4px;
  animation: fadeUp .8s .3s ease both;
}
.hero-intro {
  max-width: 560px; margin: 2rem auto 0;
  font-size: .95rem; line-height: 1.8; color: var(--text);
  opacity: .8;
  animation: fadeUp .8s .45s ease both;
}
.hero-cta {
  margin-top: 2.5rem;
  display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;
  animation: fadeUp .8s .6s ease both;
}
.btn-primary {
  background: linear-gradient(135deg, var(--blue2), var(--blue));
  color: #fff; border: none; border-radius: 6px;
  padding: .7rem 1.8rem; font-size: .9rem; font-weight: 500;
  cursor: pointer; text-decoration: none;
  transition: opacity .2s, transform .2s;
}
.btn-primary:hover { opacity: .85; transform: translateY(-2px); }
.btn-outline {
  border: 1px solid var(--border); color: var(--blue);
  border-radius: 6px; padding: .7rem 1.8rem; font-size: .9rem;
  cursor: pointer; text-decoration: none; background: transparent;
  transition: background .2s, transform .2s;
}
.btn-outline:hover { background: rgba(0,195,255,0.07); transform: translateY(-2px); }

/* ── STATS ROW ── */
.stats-row {
  position: relative; z-index: 1;
  display: flex; justify-content: center; flex-wrap: wrap; gap: 1.5rem;
  padding: 2rem 5% 4rem;
}
.stat-card {
  flex: 1; min-width: 140px; max-width: 200px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.4rem 1rem;
  text-align: center;
  animation: fadeUp .6s ease both;
}
.stat-num {
  font-family: 'Orbitron', sans-serif;
  font-size: 2rem; font-weight: 900;
  color: var(--blue);
}
.stat-label { font-size: .78rem; color: var(--muted); margin-top: .3rem; letter-spacing: 1px; }

/* ── SECTIONS ── */
section { position: relative; z-index: 1; padding: 5rem 5%; }
.section-header { text-align: center; margin-bottom: 3rem; }
.section-tag {
  display: inline-block;
  font-size: .7rem; letter-spacing: 3px; text-transform: uppercase;
  color: var(--blue); margin-bottom: .8rem;
}
.section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: clamp(1.4rem, 3vw, 2rem);
  font-weight: 700; color: #fff;
}
.section-line {
  width: 48px; height: 2px;
  background: linear-gradient(90deg, var(--blue2), var(--blue));
  margin: 1rem auto 0;
}

/* ── MEMBERS GRID ── */
.members-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.2rem;
  max-width: 1100px; margin: 0 auto;
}
.member-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.6rem 1.2rem 1.4rem;
  text-align: center;
  transition: border-color .2s, transform .2s;
  cursor: default;
}
.member-card:hover { border-color: var(--blue); transform: translateY(-4px); }
.member-number {
  font-family: 'Orbitron', sans-serif;
  font-size: 2.2rem; font-weight: 900;
  color: rgba(0,195,255,0.25);
  line-height: 1;
}
.member-name {
  font-size: 1.05rem; font-weight: 700; color: #fff;
  margin: .5rem 0 .2rem;
}
.member-pos {
  font-size: .78rem; color: var(--blue);
  border: 1px solid var(--border);
  border-radius: 99px; padding: .15rem .7rem;
  display: inline-block; margin-bottom: .8rem;
}
.member-grade { font-size: .8rem; color: var(--muted); }
.member-stats {
  display: flex; justify-content: center; gap: 1.5rem;
  margin-top: 1rem; padding-top: 1rem;
  border-top: 1px solid var(--border);
}
.mstat-val {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.1rem; color: var(--blue); font-weight: 700;
}
.mstat-label { font-size: .68rem; color: var(--muted); }

/* ── MATCHES ── */
.matches-wrap { max-width: 800px; margin: 0 auto; display: flex; flex-direction: column; gap: .8rem; }
.match-row {
  display: flex; align-items: center; gap: 1rem;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem 1.4rem;
  transition: border-color .2s;
}
.match-row:hover { border-color: var(--border); }
.match-date { font-size: .78rem; color: var(--muted); min-width: 70px; }
.match-teams { flex: 1; font-size: .95rem; color: var(--text); }
.match-home { font-size: .7rem; color: var(--muted); margin-left: .5rem; }
.match-score {
  font-family: 'Orbitron', sans-serif;
  font-size: 1rem; font-weight: 700; min-width: 48px; text-align: center;
}
.match-badge {
  font-size: .72rem; font-weight: 500; letter-spacing: 1px;
  padding: .2rem .6rem; border-radius: 4px; min-width: 36px; text-align: center;
}
.win  { background: rgba(0,230,118,.1);  color: var(--win);  border: 1px solid rgba(0,230,118,.3); }
.draw { background: rgba(255,202,40,.1); color: var(--draw); border: 1px solid rgba(255,202,40,.3); }
.loss { background: rgba(255,82,82,.1);  color: var(--loss); border: 1px solid rgba(255,82,82,.3); }
.soon-badge { background: rgba(0,195,255,.1); color: var(--soon); border: 1px solid rgba(0,195,255,.3); }

/* ── NEWS ── */
.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.4rem;
  max-width: 1000px; margin: 0 auto;
}
.news-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 1.6rem;
  transition: border-color .2s, transform .2s;
}
.news-card:hover { border-color: var(--blue); transform: translateY(-3px); }
.news-date { font-size: .75rem; color: var(--muted); margin-bottom: .6rem; }
.news-title { font-size: 1rem; font-weight: 700; color: #fff; line-height: 1.5; margin-bottom: .7rem; }
.news-summary { font-size: .85rem; color: var(--muted); line-height: 1.7; }

/* ── FOOTER ── */
footer {
  position: relative; z-index: 1;
  text-align: center;
  padding: 2.5rem 5%;
  border-top: 1px solid var(--border);
  color: var(--muted); font-size: .82rem;
}

/* ── ANIMATIONS ── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}
.fade-in { animation: fadeUp .6s ease both; }

/* scroll reveal */
.reveal { opacity: 0; transform: translateY(28px); transition: opacity .6s ease, transform .6s ease; }
.reveal.visible { opacity: 1; transform: none; }

/* ── MOBILE ── */
@media (max-width: 640px) {
  .nav-links { display: none; }
  .match-date { display: none; }
}
</style>
</head>
<body>

<nav>
  <a class="nav-logo" href="#hero">⚽ {{ team_name }}</a>
  <ul class="nav-links">
    <li><a href="#members">球员</a></li>
    <li><a href="#matches">赛程</a></li>
    <li><a href="#news">动态</a></li>
  </ul>
</nav>

<!-- HERO -->
<section id="hero">
  <div class="hero-glow"></div>
  <div class="hero-badge">Official Website</div>
  <h1 class="hero-title">⚽ <span>{{ team_name }}</span></h1>
  <p class="hero-slogan">{{ team_slogan }}</p>
  <p class="hero-intro">{{ team_intro }}</p>
  <div class="hero-cta">
    <a href="#members" class="btn-primary">认识球员</a>
    <a href="#matches" class="btn-outline">查看赛程</a>
  </div>
</section>

<!-- STATS -->
<div class="stats-row">
  {% set wins  = matches | selectattr('status','eq','胜') | list | length %}
  {% set draws = matches | selectattr('status','eq','平') | list | length %}
  {% set losses= matches | selectattr('status','eq','负') | list | length %}
  {% set goals = members | sum(attribute='goals') %}
  <div class="stat-card reveal"><div class="stat-num">{{ wins }}</div><div class="stat-label">胜场</div></div>
  <div class="stat-card reveal"><div class="stat-num">{{ draws }}</div><div class="stat-label">平局</div></div>
  <div class="stat-card reveal"><div class="stat-num">{{ losses }}</div><div class="stat-label">负场</div></div>
  <div class="stat-card reveal"><div class="stat-num">{{ goals }}</div><div class="stat-label">总进球</div></div>
  <div class="stat-card reveal"><div class="stat-num">{{ members | length }}</div><div class="stat-label">球队人数</div></div>
</div>

<!-- MEMBERS -->
<section id="members">
  <div class="section-header reveal">
    <div class="section-tag">Squad</div>
    <div class="section-title">球员阵容</div>
    <div class="section-line"></div>
  </div>
  <div class="members-grid">
    {% for m in members %}
    <div class="member-card reveal">
      <div class="member-number">#{{ m.number }}</div>
      <div class="member-name">{{ m.name }}</div>
      <span class="member-pos">{{ m.position }}</span>
      <div class="member-grade">{{ m.grade }}</div>
      <div class="member-stats">
        <div><div class="mstat-val">{{ m.goals }}</div><div class="mstat-label">进球</div></div>
        <div><div class="mstat-val">{{ m.assists }}</div><div class="mstat-label">助攻</div></div>
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<!-- MATCHES -->
<section id="matches">
  <div class="section-header reveal">
    <div class="section-tag">Schedule & Results</div>
    <div class="section-title">赛程 & 结果</div>
    <div class="section-line"></div>
  </div>
  <div class="matches-wrap">
    {% for m in matches %}
    <div class="match-row reveal">
      <span class="match-date">{{ m.date }}</span>
      <span class="match-teams">
        {% if m.home %}卢一足球队 vs {{ m.opponent }}{% else %}{{ m.opponent }} vs 卢一足球队{% endif %}
        <span class="match-home">{{ '主场' if m.home else '客场' }}</span>
      </span>
      <span class="match-score" style="color:{% if m.status=='胜' %}var(--win){% elif m.status=='平' %}var(--draw){% elif m.status=='负' %}var(--loss){% else %}var(--blue){% endif %}">{{ m.score }}</span>
      <span class="match-badge {% if m.status=='胜' %}win{% elif m.status=='平' %}draw{% elif m.status=='负' %}loss{% else %}soon-badge{% endif %}">{{ m.status }}</span>
    </div>
    {% endfor %}
  </div>
</section>

<!-- NEWS -->
<section id="news">
  <div class="section-header reveal">
    <div class="section-tag">News & Updates</div>
    <div class="section-title">球队动态</div>
    <div class="section-line"></div>
  </div>
  <div class="news-grid">
    {% for n in news %}
    <div class="news-card reveal">
      <div class="news-date">{{ n.date }}</div>
      <div class="news-title">{{ n.title }}</div>
      <div class="news-summary">{{ n.summary }}</div>
    </div>
    {% endfor %}
  </div>
</section>

<footer>
  <p>© 2025 {{ team_name }} · All Rights Reserved</p>
  <p style="margin-top:.4rem;opacity:.5">Built with Flask & Vercel</p>
</footer>

<script>
const observer = new IntersectionObserver(entries => {
  entries.forEach((e, i) => {
    if (e.isIntersecting) {
      setTimeout(() => e.target.classList.add('visible'), i * 60);
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.1 });
document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        team_name=TEAM_NAME,
        team_slogan=TEAM_SLOGAN,
        team_intro=TEAM_INTRO,
        members=MEMBERS,
        matches=MATCHES,
        news=NEWS,
    )

if __name__ == "__main__":
    app.run(debug=True)
