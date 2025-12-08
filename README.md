# riven_sniper

An automated [Warframe](https://www.warframe.com/) [riven mod](https://warframe.fandom.com/wiki/Riven_Mods) deal finder. Continuously scrapes [riven.market](https://riven.market/) and [warframe.market](https://warframe.market/), identifies top-tier stats combinations (godrolls) from historical pricing data, and sends instant [Discord](https://discord.com/) alterts when underpriced rivens appear. Runs on a [Raspberry Pi](https://www.raspberrypi.com/) with minutely polling to catch good deals before they're gone.

<!-- CODE_STATISTICS_START -->

### Code Statistics

```
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           6            184            120            528
Markdown                         1             10              4             27
-------------------------------------------------------------------------------
SUM:                             7            194            124            555
-------------------------------------------------------------------------------
```
<!-- CODE_STATISTICS_END -->

<!-- PROJECT_STRUCTURE_START -->

### Project Structure

```
riven_sniper
├── aggregator.py
├── config.py
├── logs
├── market.db
├── monitor.py
├── poller.py
├── README.md
├── riven_sniper.py
└── scraper.py

2 directories, 8 files
```
<!-- PROJECT_STRUCTURE_END -->
