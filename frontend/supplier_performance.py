# supplier_performance.py
st.title("📊 Supplier Performance Analytics")

response = requests.get(f"{API_URL}/reports/supplier_performance/", headers=headers)
data = pd.DataFrame(response.json())

if not data.empty:
    st.subheader("Supplier Reliability Report")
    st.table(data)

    chart = alt.Chart(data).mark_bar().encode(
        x="supplier",
        y="reliability_score",
        color="supplier"
    ).properties(title="Supplier Reliability Scores")
    st.altair_chart(chart, use_container_width=True)
else:
    st.write("No supplier performance data yet.")
