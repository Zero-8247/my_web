from flask import Flask, render_template_string

app = Flask(__name__)

# ── 球队数据（直接在这里修改）─────────────────────────────────────
TEAM_NAME = "卢湾一中心足球队"
TEAM_SLOGAN = "团结 · 拼搏 · 荣耀"
TEAM_INTRO = "卢湾一中心足球队代表学校参加市级及区级各类足球赛事。我们相信足球不只是运动，更是培养团队精神与拼搏意志的舞台。"

MEMBERS = [
    {"name": "张伟",  "number": 1,  "position": "守门员",   "grade": "高三", "goals": 0,  "assists": 2},
    {"name": "李明",  "number": 5,  "position": "中后卫",   "grade": "高二", "goals": 2,  "assists": 1},
    {"name": "王磊",  "number": 8,  "position": "中场核心", "grade": "高三", "goals": 7,  "assists": 9},
    {"name": "陈浩",  "number": 10, "position": "前锋",     "grade": "高二", "goals": 12, "assists": 5},
    {"name": "刘阳",  "number": 11, "position": "左边锋",   "grade": "高一", "goals": 8,  "assists": 6},
    {"name": "赵强",  "number": 4,  "position": "右后卫",   "grade": "高二", "goals": 1,  "assists": 4},
]

MATCHES = [
    {"date": "2025-03-15", "opponent": "二中足球队",   "home": True,  "score": "3-1", "status": "胜"},
    {"date": "2025-03-22", "opponent": "三中足球队",   "home": False, "score": "2-2", "status": "平"},
    {"date": "2025-04-05", "opponent": "四中足球队",   "home": True,  "score": "1-0", "status": "胜"},
    {"date": "2025-04-19", "opponent": "五中足球队",   "home": False, "score": "0-2", "status": "负"},
    {"date": "2025-05-10", "opponent": "市联赛半决赛", "home": True,  "score": "—",   "status": "即将"},
    {"date": "2025-05-24", "opponent": "市联赛决赛",   "home": True,  "score": "—",   "status": "即将"},
]

NEWS = [
    {"date": "2025-04-06", "title": "卢一足球队以1-0险胜四中，晋级半决赛！",
     "summary": "昨日主场，队长王磊在下半场第72分钟打入制胜球，全队奋勇拼搏，成功晋级市联赛半决赛。"},
    {"date": "2025-03-23", "title": "客场平局，积分榜稳居前三",
     "summary": "在三中客场的比赛中，双方各进两球，我队凭借顽强意志平局收场，积分榜排名稳居前三。"},
    {"date": "2025-03-10", "title": "新赛季训练正式开始，全队士气高昂",
     "summary": "新赛季集训正式启动，全队球员参与，教练组制定了详细的训练计划，全力备战市级联赛。"},
]
# ──────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{ team_name }} — 官方网站</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
:root {
  --blue:   #1a7fd4;
  --blue2:  #0d5fa3;
  --blue3:  #0a4a80;
  --white:  #ffffff;
  --sky:    #e4f1fb;
  --text:   #1a3a5c;
  --muted:  #5a85aa;
  --border: rgba(26,127,212,0.15);
  --shadow: 0 8px 32px rgba(26,127,212,0.12);
  --win:    #1a9e5c;
  --draw:   #e08a00;
  --loss:   #d13030;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:'Noto Sans SC',sans-serif;background:var(--sky);color:var(--text);min-height:100vh;overflow-x:hidden}

body::before{content:'';position:fixed;inset:0;z-index:0;
  background:linear-gradient(180deg,#b8ddf5 0%,#d4ecf9 25%,#e8f5fd 55%,#f4faff 100%);
  pointer-events:none}

/* ── 云朵 ── */
.clouds-bg{position:fixed;inset:0;z-index:0;pointer-events:none;overflow:hidden}
.c{position:absolute}
@keyframes drift1{0%,100%{transform:translateX(0)}50%{transform:translateX(35px)}}
@keyframes drift2{0%,100%{transform:translateX(0)}50%{transform:translateX(-28px)}}
@keyframes drift3{0%,100%{transform:translateX(0)}50%{transform:translateX(20px)}}

/* ── NAV ── */
nav{position:fixed;top:0;left:0;right:0;z-index:100;
  display:flex;align-items:center;justify-content:space-between;
  padding:0 6%;height:64px;
  background:rgba(255,255,255,0.85);backdrop-filter:blur(16px);
  border-bottom:1px solid rgba(26,127,212,0.1);
  box-shadow:0 2px 20px rgba(26,127,212,0.08)}
.nav-logo{font-family:'Bebas Neue',sans-serif;font-size:1.25rem;letter-spacing:3px;
  color:var(--blue2);text-decoration:none;display:flex;align-items:center;gap:.5rem}
.nav-logo em{font-family:'Noto Sans SC',sans-serif;font-style:normal;font-size:.78rem;
  font-weight:500;letter-spacing:1px;color:var(--muted)}
.nav-links{display:flex;gap:2.2rem;list-style:none}
.nav-links a{color:var(--muted);font-size:.83rem;font-weight:500;letter-spacing:1px;
  text-decoration:none;text-transform:uppercase;transition:color .2s;position:relative}
.nav-links a::after{content:'';position:absolute;bottom:-4px;left:0;right:0;height:2px;
  background:var(--blue);transform:scaleX(0);transition:transform .2s;border-radius:2px}
.nav-links a:hover{color:var(--blue)}
.nav-links a:hover::after{transform:scaleX(1)}

/* ── HERO ── */
#hero{position:relative;z-index:1;min-height:100vh;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  text-align:center;padding:80px 5% 60px}
.hero-ball{width:96px;height:96px;
  background:linear-gradient(135deg,var(--blue),var(--blue2));
  border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:2.6rem;box-shadow:0 8px 32px rgba(26,127,212,0.35),0 0 0 10px rgba(26,127,212,0.1);
  margin:0 auto 2rem;animation:float 4s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.hero-badge{font-size:.75rem;letter-spacing:4px;text-transform:uppercase;color:var(--blue);
  font-weight:500;background:rgba(26,127,212,0.08);border:1px solid rgba(26,127,212,0.2);
  padding:.35rem 1.4rem;border-radius:99px;display:inline-block;margin-bottom:1.4rem;
  animation:fadeUp .7s ease both}
h1.hero-title{font-family:'Bebas Neue',sans-serif;
  font-size:clamp(3rem,10vw,7rem);letter-spacing:8px;line-height:1;
  color:var(--blue2);text-shadow:0 4px 24px rgba(26,127,212,0.2);
  animation:fadeUp .7s .1s ease both}
.hero-slogan{margin-top:.8rem;font-size:1rem;color:var(--muted);letter-spacing:5px;
  animation:fadeUp .7s .2s ease both}
.divider{display:flex;align-items:center;justify-content:center;gap:.8rem;
  margin:1.8rem auto;animation:fadeUp .7s .3s ease both}
.divider::before,.divider::after{content:'';width:60px;height:1px;
  background:linear-gradient(90deg,transparent,rgba(26,127,212,0.4))}
.divider::after{background:linear-gradient(90deg,rgba(26,127,212,0.4),transparent)}
.hero-intro{max-width:500px;margin:0 auto 2.5rem;font-size:.95rem;line-height:1.9;
  color:var(--muted);animation:fadeUp .7s .4s ease both}
.cta{display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;animation:fadeUp .7s .5s ease both}
.btn-p{background:linear-gradient(135deg,var(--blue),var(--blue2));color:#fff;border:none;
  border-radius:8px;padding:.78rem 2.2rem;font-size:.9rem;font-weight:500;cursor:pointer;
  text-decoration:none;box-shadow:0 4px 18px rgba(26,127,212,0.35);
  transition:transform .2s,box-shadow .2s;font-family:'Noto Sans SC',sans-serif}
.btn-p:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(26,127,212,0.42)}
.btn-o{border:2px solid var(--blue);color:var(--blue);border-radius:8px;padding:.74rem 2.2rem;
  font-size:.9rem;font-weight:500;cursor:pointer;text-decoration:none;
  background:rgba(255,255,255,0.85);transition:background .2s,transform .2s;
  font-family:'Noto Sans SC',sans-serif}
.btn-o:hover{background:rgba(26,127,212,0.07);transform:translateY(-2px)}

/* ── STATS ── */
.stats{position:relative;z-index:1;display:flex;justify-content:center;
  flex-wrap:wrap;gap:1.2rem;padding:0 5% 5rem}
.scard{flex:1;min-width:130px;max-width:175px;background:var(--white);
  border:1px solid var(--border);border-radius:16px;padding:1.6rem 1rem 1.4rem;
  text-align:center;box-shadow:var(--shadow);position:relative;overflow:hidden}
.scard::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--blue),#7ec8f0)}
.snum{font-family:'Bebas Neue',sans-serif;font-size:2.6rem;letter-spacing:2px;
  color:var(--blue2);line-height:1}
.slabel{font-size:.76rem;color:var(--muted);margin-top:.4rem;letter-spacing:1px}

/* ── SECTION ── */
section{position:relative;z-index:1;padding:5rem 5%}
.sh{text-align:center;margin-bottom:3.5rem}
.stag{display:inline-block;font-size:.7rem;letter-spacing:3px;text-transform:uppercase;
  color:var(--blue);margin-bottom:.8rem;font-weight:500}
.stitle{font-family:'Bebas Neue',sans-serif;font-size:clamp(1.8rem,4vw,2.6rem);
  letter-spacing:4px;color:var(--blue2)}
.sline{display:flex;align-items:center;justify-content:center;gap:.8rem;margin-top:1rem}
.sline::before,.sline::after{content:'';width:36px;height:1px;
  background:linear-gradient(90deg,transparent,rgba(26,127,212,0.4))}
.sline::after{background:linear-gradient(90deg,rgba(26,127,212,0.4),transparent)}

/* ── MEMBERS ── */
.mgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));
  gap:1.4rem;max-width:1100px;margin:0 auto}
.mcard{background:var(--white);border:1px solid var(--border);border-radius:20px;
  padding:1.8rem 1.2rem 1.5rem;text-align:center;box-shadow:var(--shadow);
  transition:transform .25s,box-shadow .25s;position:relative;overflow:hidden}
.mcard::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;
  background:linear-gradient(90deg,var(--blue),#7ec8f0);
  transform:scaleX(0);transition:transform .25s}
.mcard:hover{transform:translateY(-6px);box-shadow:0 16px 48px rgba(26,127,212,0.18)}
.mcard:hover::after{transform:scaleX(1)}
.mnum{font-family:'Bebas Neue',sans-serif;font-size:3.2rem;letter-spacing:2px;
  color:rgba(26,127,212,0.1);line-height:1}
.mname{font-size:1.1rem;font-weight:700;color:var(--text);margin:.4rem 0 .5rem}
.mpos{font-size:.74rem;font-weight:500;color:var(--blue);
  background:rgba(26,127,212,0.08);border:1px solid rgba(26,127,212,0.2);
  border-radius:99px;padding:.2rem .8rem;display:inline-block;margin-bottom:.6rem}
.mgrade{font-size:.8rem;color:var(--muted)}
.mstats{display:flex;justify-content:center;gap:1.5rem;margin-top:1rem;
  padding-top:1rem;border-top:1px solid var(--border)}
.mv{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;letter-spacing:1px;color:var(--blue2)}
.ml{font-size:.68rem;color:var(--muted);margin-top:.1rem}

/* ── MATCHES ── */
.mwrap{max-width:780px;margin:0 auto;display:flex;flex-direction:column;gap:.9rem}
.mrow{display:flex;align-items:center;gap:1rem;background:var(--white);
  border:1px solid var(--border);border-radius:12px;padding:1.1rem 1.6rem;
  box-shadow:0 2px 12px rgba(26,127,212,0.06);transition:box-shadow .2s,transform .2s}
.mrow:hover{box-shadow:0 6px 24px rgba(26,127,212,0.14);transform:translateX(4px)}
.mdate{font-size:.78rem;color:var(--muted);min-width:76px;font-weight:500}
.mteams{flex:1;font-size:.92rem;color:var(--text);font-weight:500}
.mhome{font-size:.68rem;color:var(--blue);background:rgba(26,127,212,0.08);
  border-radius:4px;padding:.1rem .4rem;margin-left:.5rem;font-weight:500}
.mscore{font-family:'Bebas Neue',sans-serif;font-size:1.1rem;letter-spacing:2px;
  min-width:52px;text-align:center}
.mbadge{font-size:.72rem;font-weight:600;letter-spacing:1px;
  padding:.25rem .7rem;border-radius:6px;min-width:40px;text-align:center}
.win {background:#e8f8ef;color:var(--win); border:1px solid rgba(26,158,92,.25)}
.draw{background:#fdf3e3;color:var(--draw);border:1px solid rgba(224,138,0,.25)}
.loss{background:#fdeaea;color:var(--loss);border:1px solid rgba(209,48,48,.25)}
.soon{background:rgba(26,127,212,.08);color:var(--blue);border:1px solid rgba(26,127,212,.25)}

/* ── NEWS ── */
.ngrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));
  gap:1.5rem;max-width:1000px;margin:0 auto}
.ncard{background:var(--white);border:1px solid var(--border);border-radius:20px;
  padding:1.8rem;box-shadow:var(--shadow);transition:transform .25s,box-shadow .25s;
  position:relative;overflow:hidden}
.ncard::before{content:'☁';position:absolute;bottom:.8rem;right:1.2rem;
  font-size:2rem;opacity:.1;pointer-events:none}
.ncard:hover{transform:translateY(-4px);box-shadow:0 12px 40px rgba(26,127,212,0.16)}
.ndate{font-size:.74rem;color:var(--blue);background:rgba(26,127,212,0.07);
  border-radius:6px;padding:.2rem .6rem;display:inline-block;margin-bottom:.8rem;font-weight:500}
.ntitle{font-size:1rem;font-weight:700;color:var(--text);line-height:1.55;margin-bottom:.7rem}
.nsummary{font-size:.85rem;color:var(--muted);line-height:1.8}

/* ── FOOTER ── */
footer{position:relative;z-index:1;text-align:center;padding:3rem 5%;
  background:var(--white);border-top:1px solid var(--border)}
.flogo{font-family:'Bebas Neue',sans-serif;font-size:1.4rem;letter-spacing:4px;
  color:var(--blue2);margin-bottom:.5rem}
footer p{font-size:.82rem;color:var(--muted);line-height:2.2}

/* ── UTILS ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.reveal{opacity:0;transform:translateY(24px);transition:opacity .65s ease,transform .65s ease}
.reveal.visible{opacity:1;transform:none}
.glass{background:rgba(255,255,255,0.45);backdrop-filter:blur(10px)}
@media(max-width:640px){.nav-links{display:none}.mdate{display:none}h1.hero-title{letter-spacing:3px}}
</style>
</head>
<body>

<!-- 云朵背景 -->
<div class="clouds-bg" aria-hidden="true">
  <div class="c" style="top:4%;left:-1%;opacity:.6;animation:drift1 18s ease-in-out infinite">
    <svg width="340" height="110" viewBox="0 0 340 110"><ellipse cx="170" cy="78" rx="148" ry="40" fill="white"/><ellipse cx="105" cy="60" rx="75" ry="48" fill="white"/><ellipse cx="215" cy="54" rx="85" ry="50" fill="white"/><ellipse cx="155" cy="44" rx="65" ry="42" fill="white"/></svg>
  </div>
  <div class="c" style="top:3%;right:-2%;opacity:.55;animation:drift2 22s ease-in-out infinite">
    <svg width="300" height="96" viewBox="0 0 300 96"><ellipse cx="150" cy="68" rx="128" ry="34" fill="white"/><ellipse cx="92" cy="52" rx="66" ry="42" fill="white"/><ellipse cx="188" cy="48" rx="76" ry="44" fill="white"/><ellipse cx="136" cy="38" rx="55" ry="36" fill="white"/></svg>
  </div>
  <div class="c" style="top:20%;left:8%;opacity:.38;animation:drift3 28s ease-in-out infinite">
    <svg width="200" height="66" viewBox="0 0 200 66"><ellipse cx="100" cy="48" rx="86" ry="24" fill="white"/><ellipse cx="62" cy="36" rx="48" ry="32" fill="white"/><ellipse cx="130" cy="32" rx="54" ry="34" fill="white"/></svg>
  </div>
  <div class="c" style="top:32%;right:3%;opacity:.32;animation:drift1 32s ease-in-out infinite">
    <svg width="160" height="54" viewBox="0 0 160 54"><ellipse cx="80" cy="40" rx="68" ry="20" fill="white"/><ellipse cx="50" cy="30" rx="38" ry="26" fill="white"/><ellipse cx="105" cy="26" rx="44" ry="28" fill="white"/></svg>
  </div>
  <div class="c" style="bottom:18%;left:4%;opacity:.42;animation:drift2 20s ease-in-out infinite">
    <svg width="280" height="88" viewBox="0 0 280 88"><ellipse cx="140" cy="64" rx="120" ry="30" fill="white"/><ellipse cx="86" cy="48" rx="62" ry="40" fill="white"/><ellipse cx="178" cy="44" rx="70" ry="42" fill="white"/><ellipse cx="128" cy="34" rx="52" ry="34" fill="white"/></svg>
  </div>
  <div class="c" style="bottom:6%;right:6%;opacity:.38;animation:drift3 24s ease-in-out infinite">
    <svg width="220" height="72" viewBox="0 0 220 72"><ellipse cx="110" cy="52" rx="94" ry="26" fill="white"/><ellipse cx="68" cy="40" rx="52" ry="34" fill="white"/><ellipse cx="144" cy="36" rx="60" ry="36" fill="white"/></svg>
  </div>
</div>

<!-- NAV -->
<nav>
  <a class="nav-logo" href="#hero">⚽ {{ team_name }} <em>OFFICIAL</em></a>
  <ul class="nav-links">
    <li><a href="#members">球员</a></li>
    <li><a href="#matches">赛程</a></li>
    <li><a href="#news">动态</a></li>
  </ul>
</nav>

<!-- HERO -->
<section id="hero">
  <div class="hero-ball">⚽</div>
  <div class="hero-badge">卢湾一中心 · 足球校队</div>
  <h1 class="hero-title">{{ team_name }}</h1>
  <p class="hero-slogan">{{ team_slogan }}</p>
  <div class="divider"><span style="font-size:1.1rem">☁️</span></div>
  <p class="hero-intro">{{ team_intro }}</p>
  <div class="cta">
    <a href="#members" class="btn-p">认识球员</a>
    <a href="#matches" class="btn-o">查看赛程</a>
  </div>
</section>

<!-- STATS -->
<div class="stats">
  {% set wins   = matches|selectattr('status','eq','胜')|list|length %}
  {% set draws  = matches|selectattr('status','eq','平')|list|length %}
  {% set losses = matches|selectattr('status','eq','负')|list|length %}
  {% set goals  = members|sum(attribute='goals') %}
  <div class="scard reveal"><div class="snum">{{ wins }}</div><div class="slabel">☁ 胜场</div></div>
  <div class="scard reveal"><div class="snum">{{ draws }}</div><div class="slabel">☁ 平局</div></div>
  <div class="scard reveal"><div class="snum">{{ losses }}</div><div class="slabel">☁ 负场</div></div>
  <div class="scard reveal"><div class="snum">{{ goals }}</div><div class="slabel">☁ 总进球</div></div>
  <div class="scard reveal"><div class="snum">{{ members|length }}</div><div class="slabel">☁ 球队人数</div></div>
</div>

<!-- MEMBERS -->
<section id="members" class="glass">
  <div class="sh reveal">
    <div class="stag">Squad · 阵容</div>
    <div class="stitle">球员阵容</div>
    <div class="sline"><span>⚽</span></div>
  </div>
  <div class="mgrid">
    {% for m in members %}
    <div class="mcard reveal">
      <div class="mnum">#{{ m.number }}</div>
      <div class="mname">{{ m.name }}</div>
      <span class="mpos">{{ m.position }}</span>
      <div class="mgrade">{{ m.grade }}</div>
      <div class="mstats">
        <div><div class="mv">{{ m.goals }}</div><div class="ml">进球</div></div>
        <div><div class="mv">{{ m.assists }}</div><div class="ml">助攻</div></div>
      </div>
    </div>
    {% endfor %}
  </div>
</section>

<!-- MATCHES -->
<section id="matches">
  <div class="sh reveal">
    <div class="stag">Schedule · 赛程</div>
    <div class="stitle">赛程 & 结果</div>
    <div class="sline"><span>🏆</span></div>
  </div>
  <div class="mwrap">
    {% for m in matches %}
    <div class="mrow reveal">
      <span class="mdate">{{ m.date }}</span>
      <span class="mteams">
        {% if m.home %}卢湾一中心 vs {{ m.opponent }}{% else %}{{ m.opponent }} vs 卢湾一中心{% endif %}
        <span class="mhome">{{ '主场' if m.home else '客场' }}</span>
      </span>
      <span class="mscore" style="color:{% if m.status=='胜' %}var(--win){% elif m.status=='平' %}var(--draw){% elif m.status=='负' %}var(--loss){% else %}var(--blue){% endif %}">{{ m.score }}</span>
      <span class="mbadge {% if m.status=='胜' %}win{% elif m.status=='平' %}draw{% elif m.status=='负' %}loss{% else %}soon{% endif %}">{{ m.status }}</span>
    </div>
    {% endfor %}
  </div>
</section>

<!-- NEWS -->
<section id="news" class="glass">
  <div class="sh reveal">
    <div class="stag">News · 动态</div>
    <div class="stitle">球队动态</div>
    <div class="sline"><span>📰</span></div>
  </div>
  <div class="ngrid">
    {% for n in news %}
    <div class="ncard reveal">
      <div class="ndate">{{ n.date }}</div>
      <div class="ntitle">{{ n.title }}</div>
      <div class="nsummary">{{ n.summary }}</div>
    </div>
    {% endfor %}
  </div>
</section>

<!-- FOOTER -->
<footer>
  <div class="flogo">⚽ 卢湾一中心足球队</div>
  <p>团结 · 拼搏 · 荣耀</p>
  <p style="opacity:.55">© 2025 卢湾一中心足球队 · All Rights Reserved</p>
</footer>

<script>
const io = new IntersectionObserver(entries => {
  entries.forEach((e,i) => {
    if(e.isIntersecting){
      setTimeout(()=>e.target.classList.add('visible'), i*80);
      io.unobserve(e.target);
    }
  });
},{threshold:0.08});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
</body>
</html>"""

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
