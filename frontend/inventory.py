# inventory.py
st.title("📦 Inventory Management")

# Add product
st.header("Add Product")
name = st.text_input("Product Name")
price = st.number_input("Price", min_value=0.0)
stock = st.number_input("Initial Stock", min_value=0)
reorder_level = st.number_input("Reorder Level", min_value=1)
if st.button("Add Product"):
    response = requests.post(f"{API_URL}/products/", params={
        "name": name, "price": price, "stock": stock, "reorder_level": reorder_level
    }, headers=headers)
    st.write(response.json())

# Low stock report
st.header("Low Stock Alerts")
response = requests.get(f"{API_URL}/reports/low_stock/", headers=headers)
data = pd.DataFrame(response.json())
if not data.empty:
    st.table(data)
else:
    st.write("✅ All products are sufficiently stocked")
