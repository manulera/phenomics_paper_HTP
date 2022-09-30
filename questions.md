## Questions

### Phenotypes in control condition with phloxin

I guess we would need the new terms: decreased viability during vegetative growth / increased viability during vegetative growth

### Glucose levels

In the datasete there are several conditions that use different glucose concentrations:

```
> Knockouts
YESphlox-Temp25Gluc0.1		0.1% glucose in media + grown at 25°C
YESphlox-Temp25Gluc0.5		0.5% glucose in media + grown at 25°C
YESphlox-Temp25Gluc1		1% glucose in media + grown at 25°C
YESphlox-Temp25Gluc3		3% glucose in media + grown at 25°C

YESphlox-Gluc0.1stationary7CdCl1		0.1% glucose in media + grown for 7d + 1mM cadmium chloride
YESphlox-Xylose2	2	Xylose as carbon source with 0.1% starter glucose
YESphlox-Gluc0.5starionary7		0.5% glucose in media + grown for 7d 
YESphlox-Gluc1stationary7		1% glucose in media + grown for 7d 
YESphlox-stationary7		Grown for 7 days

> OE
EMM_Gluc0.5
EMM_Gluc2
EMM_Gluc3

```

The problem, is we only have these conditions:


```
id: FYECO:0000104
name: low glucose MM
def: "Experiments were performed in minimal medium containing a low concentration of glucose (~0.5%) as carbon source, salts and water."

id: FYECO:0000126
name: glucose MM
alt_id: FYECO:0000014
def: "Experiments were performed in medium containing glucose (typically <2% w/v), salts, and water, and may be supplemented with additional amino acids." [PomBase:al]

id: FYECO:0000016
name: high glucose MM
def: "Experiments were performed in minimal medium containing a high concentration of glucose (~5-8% typically) as carbon source, salts and water." [PomBase:al]

id: FYECO:0000081
name: low glucose YES
def: "Experiments were performed in rich medium containing yeast extract and other components. The concentration of glucose is very low (eg around 0.1%)." [PomBase:al]

id: FYECO:0000137
name: YES
alt_id: FYECO:0000012
def: "Experiments were performed in rich medium containing yeast extract, glucose, and other components. The concentration of glucose is typically around 2-3%." [PomBase:al]

id: FYECO:0000162
name: high glucose YES
def: "Experiments were performed in rich medium containing yeast extract and other components. The concentration of glucose is high low (eg around 8%)." [PomBase:al]
```
And these phenotypes:

```
id: FYPO:0003938
name: increased cell population growth during glucose starvation
def: "A cell growth phenotype in which cell population growth is increased relative to normal under conditions of glucose starvation." [PomBase:mah]

id: FYPO:0003743
name: decreased cell population growth during glucose starvation
def: "A cell growth phenotype in which cell population growth is decreased relative to normal under conditions of glucose starvation." [PomBase:mah]

id: FYPO:0004162
name: loss of viability upon glucose starvation
def: "A cell population phenotype in which a smaller than normal proportion of cells in the population remains viable when cells the population are subject to glucose starvation." [PomBase:mah]

id: FYPO:0004163
name: increased viability upon glucose starvation
def: "A cell population phenotype in which a larger than normal proportion of cells in the population remains viable when cells the population are subject to glucose starvation." [PomBase:mah]

id: FYPO:0005231
name: loss of viability in stationary phase upon glucose starvation
def: "A cell population phenotype in which a smaller than normal proportion of cells in the population remains viable after entering stationary phase, when cells the population are subject to glucose starvation." [PMID:26624998, PomBase:mah]
```

The question is then:

* Is 0.5% or 1% glucose considered glucose starvation for phenotypes or low glucose for the medium? Our FYPO term for YE low glucose says 0.1%, for MM 0.5%.
  * If so, we can annotate those with glucose starvation, and use the condition of low glucose (we would have to change the definition).
* We can't capture the concetration of glucose right now, but we dicussed with Val to do so in the future. Therefore, for conditions in which glucose is between starvation and normal, but is neither of those, we could for now just annotate to the terms that do not mention glucose at all, and we make a note to update the concentration once it is supported.
  * Same applies to the phenotypes with 2% and 3% glucose.

## 32 and 25 temperature

* Similar to previous. We typically define the range of 25-32 as standard temperature, so for now we have no way to capture the difference between those conditions. We could make a similar change in the future to include the exact temperature in the condition, especially for HTP.

## CoCl2 condition

Is this sensitive to cobalt? Or should a term mentioning hypoxia be used?

## "Better than wild type" phenotypes

* If something is a hit, and has median_fitness_log2 > 0, this means that it grows better / has higher viability than control, right? So that would mean that in drug X, the phenotype would be resistance to drug X.

## Microscopy phenotypes

* For `significance_score_percentage_bi-nucleated`, we could create a new population phenotype `increased binucleate index`, I guess this would have a similar meaning to mitotic index. We could use `FC_dif_%_bi-nucleated` for severity.

* For `significance_score_mono-nucleated` and `significance_score_bi-nucleated` I don't know what would be the right thing to do. We can annotate to `increased cell length` if either or both are significant? Do you think it's worth to differenciate the difference in length for binucleate or mononucleate cells?

## Flow citometry phenotypes

What is a hit in the screen? I guess the phenotype here would be increased/decreased number of cells with 1C DNA content.