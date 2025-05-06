# Prisoner's Dilemma

This code implements most of the strategies from Axelrod's Tournament in 1980. It is a reproduction of the paper [Effective choice in the prisoner's dilemma](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=204c5a8ba01650496d74108ce49cd554a3880fbc), and references the [Axelrod Python](https://axelrod.readthedocs.io/en/fix-documentation/index.html) implementation. It can be used to evaluate the overall performance of different strategies in repeated Prisoner's Dilemma games.

> Note: Since the original paper did not release source code, the `Name Withheld` strategy was not implemented. Additionally, based on experimental results, some strategy implementations deviate from the descriptions in the original paper (e.g., the score of TidemanAndChieruzzi against itself suggests that it does not fully cooperate with itself — a strange observation; see Table 2, second row, second column).

[Click here to jump to the English version.](#如何使用)

---

本代码实现了 1980 年 Axelrod's Tournament（阿克塞尔罗德竞赛）中的绝大部分策略，是对论文 [Effective choice in the prisoner's dilemma](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=204c5a8ba01650496d74108ce49cd554a3880fbc) 的复现，参考了 [Axelrod Python](https://axelrod.readthedocs.io/en/fix-documentation/index.html) 的代码，可用于测试不同策略在多次可重复囚徒困境中的总体表现。

> 注：由于原论文并未开源源代码，因此其中的 `Name Withheld` 方法未能实现。此外，从实验结果来看，部分策略的实现与原论文描述不完全一致（例如：从原论文中 TidemanAndChieruzzi 方法对阵自身的分数推断，该方法并未实现完全合作，这是一个奇怪的现象；见论文 Table 2 第二行第二列）。

[点击这里跳转至中文详细介绍。](#如何使用)

---

## How to Use

Install dependencies (only a few are needed), and run `main.py`. To change parameters (e.g., select which strategies participate), modify the code under `if __name__ == "__main__":`. The results will be printed to the terminal and saved in `results.csv`.

Note: The composition of the strategy pool significantly affects final rankings (i.e., a strategy may perform well in group A but poorly in group B).

## Parameter Description

See the `parameters.py` file.

The payoff matrix used in this Prisoner's Dilemma implementation is:

```
[[(3, 3), (0, 5)],
[(5, 0), (1, 1)]]
```

That is:
1. If both players cooperate, each scores 3 points.
2. If one cooperates and the other defects, the defector gets 5 points, and the cooperator gets 0.
3. If both defect, each gets 1 point.

In the code, `0` stands for cooperation and `1` for defection.

## Strategy Summary

Strategies *1–13* and *16* come directly from the original paper.

| No.  | Strategy Name        | Description                                                  |
|------|----------------------|--------------------------------------------------------------|
| 1    | TitForTat            | Cooperate in the first round, then mimic opponent’s last move. |
| 2    | TidemanAndChieruzzi | Escalates punishment; attempts reconciliation if leading in score. |
| 3    | Nydegger             | Mimics early on; later cooperates based on weighted history. |
| 4    | Grofman              | Cooperates if both agreed last round, else cooperates with low probability. |
| 5    | Shubik               | Incrementally punishes defection until retaliation is complete. |
| 6    | SteinAndRapoport     | Starts with cooperation; tests for randomness, then adapts. |
| 7    | Grudger              | Defects forever after being betrayed once.                   |
| 8    | Davis                | Unconditionally cooperates at first; defects permanently if betrayed. |
| 9    | Graaskamp            | Defensive early game; uses statistics later to evaluate trust. |
| 10   | Downing              | Calculates expected value based on reactions to cooperation/defection. |
| 11   | Feld                 | Mimics opponent; cooperation probability linearly decreases over time. |
| 12   | Joss                 | Mostly mimics, but occasionally defects to test opponent.     |
| 13   | Tullock              | Cooperates for 11 rounds, then adjusts cooperation probability based on opponent’s recent behavior. |
| 14   | Collaborator         | Always cooperates.                                           |
| 15   | Betrayer             | Always defects.                                              |
| 16   | Random               | Randomly chooses to cooperate or defect.                     |
| 17   | TwoTitsForTat        | Defects if betrayed in either of the last two rounds.        |
| 18   | TitForTwoTats        | Defects only after being betrayed two times in a row.        |

## Extensibility

1. **Add new Prisoner’s Dilemma strategies:**
   - Create a new strategy class in `strategies.py`, implementing a `__call__` method (which takes a `Status` object as input). If extra state tracking is needed, define variables in `__init__`.
   - Add the new strategy class name to the `players` list in `main.py`.

2. **Support more flexible game settings**, e.g., no punishment for defection or equal payoffs for cooperation and defection:
   - Modify the `reward` matrix in `parameters.py`.
   - You may also need to adjust logic in some strategies’ `__call__` methods.

3. **Extend to multi-choice games** (e.g., adding a “silent” option in addition to cooperate/defect):
   - Modify the dimensions and values of the `reward` matrix in `parameters.py`.
   - Update `id_to_decision` to include mappings for new choices.
   - Modify the corresponding strategy classes to handle the new options if needed.

## Some Interesting Experimental Observations

1. When the majority of players are cooperative, exploitative strategies usually do not score well.
   - For example, the Tullock strategy (which defects with *opponent's defection rate in last 10 rounds + 10%*) performs poorly; removing the +10% actually improves its ranking.
   - Although Betrayer gets the highest score against Collaborator, its overall ranking is still low.

2. In a population of only defectors, Betrayer outperforms Collaborator.

3. Random is generally the worst-performing strategy regardless of the composition of the population.

### If you find any bugs in the code, or would like to contribute additional strategies or experimental results, feel free to open an issue or submit a pull request.

---

## 如何使用

安装依赖（所需依赖较少），运行 `main.py`。若需更改参数（例如具体选择参与策略），请在 `if __name__ == "__main__":` 后进行修改。运行结果将显示在终端并保存在 `results.csv` 文件中。

请注意：策略组合的选择会显著影响最终排名（即某策略可能在 A 群体中得分高，在 B 群体中得分低）。

## 参数介绍

见 `parameters.py` 文件。

本囚徒困境使用的支付矩阵（得分矩阵）为：

```
[[(3, 3), (0, 5)],
[(5, 0), (1, 1)]]
```

即：
1. 双方均选择合作，则各得 3 分；
2. 一方合作，另一方背叛，则背叛者得 5 分，合作者得 0 分；
3. 双方均背叛，则各得 1 分。

代码中定义 0 为合作，1 为背叛。

## 具体策略简单介绍

*1–13* 和 *16* 方法均来自原论文。

| 编号 | 策略名称           | 简要说明                                                   |
|------|--------------------|------------------------------------------------------------|
| 1    | TitForTat          | 首轮合作，之后模仿对方上一次的决策。                       |
| 2    | TidemanAndChieruzzi | 逐步加剧报复，若己方得分领先则尝试重新合作。               |
| 3    | Nydegger           | 前几轮模仿，之后根据加权历史计算是否合作。                 |
| 4    | Grofman            | 若双方上轮一致则合作，否则以小概率继续合作。               |
| 5    | Shubik             | 对背叛进行递增报复，直到完成惩罚周期。                     |
| 6    | SteinAndRapoport   | 先合作，判断对手是否随机，再选择应对策略。                 |
| 7    | Grudger            | 一旦被背叛便永久背叛。                                     |
| 8    | Davis              | 前几轮无条件合作，之后如被背叛则永久背叛。                 |
| 9    | Graaskamp          | 初期防御强烈，后期根据统计判断是否信任对方。               |
| 10   | Downing            | 根据对手对合作与背叛的反应来估算收益并决策。               |
| 11   | Feld               | 先模仿，对方合作时合作概率随时间线性下降。                 |
| 12   | Joss               | 模仿为主，偶尔背叛以测试对手。                             |
| 13   | Tullock            | 前 11 轮合作，之后根据对手近 10 轮的合作频率调整合作概率。 |
| 14   | Collaborator       | 始终合作。                                                 |
| 15   | Betrayer           | 始终背叛。                                                 |
| 16   | Random             | 随机选择合作或背叛。                                       |
| 17   | TwoTitsForTat      | 若最近两轮有一次被背叛则报复。                             |
| 18   | TitForTwoTats      | 连续两次被背叛才报复，否则合作。                           |


## 可扩展性

1. 支持添加更多囚徒困境策略：
   - 在 `strategies.py` 中新增策略类，并定义 `__call__` 方法（传入参数为 `Status` 类）。若需维护额外状态参数，可在 `__init__` 方法中定义。
   - 将新策略类的名称添加至 `main.py` 的 `players` 列表中。

2. 支持更自由的实验背景，例如：不惩罚背叛者，或让合作与背叛得分相同等：
   - 修改 `parameters.py` 中的 `reward` 支付矩阵；
   - 可能需要同步修改部分策略类中的 `__call__` 方法。

3. 可扩展为多选择博弈（如引入“沉默”选项）：
   - 修改 `parameters.py` 中的 `reward` 维度，定义新选项；
   - 更新 `id_to_decision` 中的编号与选项映射；
   - 若涉及策略行为调整，需修改相应 `__call__` 方法。

## 一些有趣的简单实验结论：

1. 当参与者中好人占比较高时，主动背叛/投机策略往往得分不高。
   - Tullock 方法（以 *前 10 步对手背叛概率 +10%* 的概率进行背叛）表现不佳；若不加 10%，排名反而更高。
   - 虽然 Betrayer 面对 Collaborator 获得全场最高分，但其总体排名并不高。

2. 在参与者中全是恶人的环境下，Betrayer 比 Collaborator 更具优势。

3. 无论在何种组合下，Random 基本都是表现最差的策略。

### 如果你发现了代码中的任何 bug，或者想要提交更多方法 or 实验结论，欢迎提出 issue 或者直接提交 PR。