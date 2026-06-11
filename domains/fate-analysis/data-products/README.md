# FateCat 数据产品

`domains/fate-analysis/data-products/` 是 FateCat 命理分析领域的静态数据产品层。

## 分区

| 路径 | 用途 | 是否默认运行依赖 |
| --- | --- | --- |
| `china_coordinates.csv` | 中国行政区经纬度数据 | 是 |
| `classics/*.txt` | 已整理命理古籍与基础语料 | 可选 |
| `calendar/solar_terms/golden/` | 节气 golden fixture，用于测试成熟历法库输出 | 测试依赖 |

## 原始资料规则

- raw 私有资料只作为本地来源资料和人工复核材料，不进入此 canonical 数据产品目录。
- raw 路径已被 `.gitignore` 和导出脚本排除，避免大文件、版权不明资料或未清洗 OCR 进入发布包。
- 后续要用于生产逻辑时，必须先完成来源复核、结构化抽取、字段契约和回归测试。
- golden fixture 只作为测试门禁，运行期仍调用 `lunar-python`。
