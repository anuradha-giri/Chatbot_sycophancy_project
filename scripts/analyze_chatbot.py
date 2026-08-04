import pandas as pd
import plotly.express as px
import json
import os

df = pd.read_csv("results.csv")

for col in ["gemini_score", "manual_score", "final_score"]:
    df[col] = df[col].astype(str).str.strip().str.upper()

label_order = ["FALSE_AGREEMENT", "OVERLY_AGREEABLE", "NEUTRAL"]

overall = df["final_score"].value_counts().reindex(label_order, fill_value=0).reset_index()
overall.columns = ["label", "count"]
overall["percent"] = (overall["count"] / len(df) * 100).round(2)

category_counts = pd.crosstab(df["category"], df["final_score"]).reindex(columns=label_order, fill_value=0).reset_index()

os.makedirs("output", exist_ok=True)
overall.to_csv("output/overall_summary.csv", index=False)
category_counts.to_csv("output/category_counts.csv", index=False)

fig = px.bar(
    overall,
    x="label",
    y="count",
    text="count",
    title="Chatbot Labels by Final Score (100 prompts)<br><span style='font-size: 18px; font-weight: normal;'>Source: results.csv | Overall distribution of response behavior</span>",
    labels={"label": "Label", "count": "Count"}
)
fig.update_traces(textposition="outside", cliponaxis=False)
fig.update_xaxes(title_text="Label")
fig.update_yaxes(title_text="Count")
fig.write_image("output/overall_labels.png")
with open("output/overall_labels.png.meta.json", "w") as f:
    json.dump({
        "caption": "Chatbot labels by final score",
        "description": "Bar chart of FALSE_AGREEMENT, OVERLY_AGREEABLE, and NEUTRAL counts across 100 prompts."
    }, f)

cat_long = category_counts.melt(id_vars=["category"], var_name="label", value_name="count")
fig2 = px.bar(
    cat_long,
    x="category",
    y="count",
    color="label",
    barmode="stack",
    title="Chatbot Labels by Category (100 prompts)<br><span style='font-size: 18px; font-weight: normal;'>Source: results.csv | Prompt groups compared by final score</span>",
    labels={"category": "Category", "count": "Count", "label": "Label"}
)
fig2.update_traces(cliponaxis=False)
fig2.update_xaxes(title_text="Category")
fig2.update_yaxes(title_text="Count")
fig2.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5))
fig2.write_image("output/category_labels.png")
with open("output/category_labels.png.meta.json", "w") as f:
    json.dump({
        "caption": "Chatbot labels by category",
        "description": "Stacked bar chart comparing FALSE_AGREEMENT, OVERLY_AGREEABLE, and NEUTRAL across prompt categories."
    }, f)

print("Done. Files saved in output/")
