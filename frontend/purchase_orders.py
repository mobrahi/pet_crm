# purchase_orders.py
st.title("📑 Purchase Orders")

# Auto-generate POs
st.header("Auto-Generate Purchase Orders")
if st.button("Generate POs"):
    response = requests.post(f"{API_URL}/purchase_orders/auto_generate/", headers=headers)
    data = pd.DataFrame(response.json())
    st.table(data)

# Future: Send PO via email
st.header("Send Purchase Order")
po_id = st.number_input("PO ID", min_value=1)
if st.button("Send PO"):
    st.write(f"📧 Sending PO #{po_id} to supplier...")
    # Here you’d integrate with an email API (e.g., SendGrid, SMTP)

# purchase_orders.py
st.header("Send Purchase Order via Email")
po_id = st.number_input("PO ID", min_value=1)
if st.button("Send PO"):
    response = requests.post(f"{API_URL}/purchase_orders/{po_id}/send/", headers=headers)
    st.write(response.json())

# purchase_orders.py
st.header("Send Purchase Order with PDF")
po_id = st.number_input("PO ID", min_value=1)
if st.button("Send PO with PDF"):
    response = requests.post(f"{API_URL}/purchase_orders/{po_id}/send_pdf/", headers=headers)
    st.write(response.json())

# purchase_orders.py
st.title("📑 Multi-Product Purchase Orders")

supplier_id = st.number_input("Supplier ID", min_value=1)
items = []

st.header("Add Products to PO")
product_id = st.number_input("Product ID", min_value=1)
quantity = st.number_input("Quantity", min_value=1)
if st.button("Add Product to PO"):
    items.append({"product_id": product_id, "quantity": quantity})
    st.write("Current items:", items)

if st.button("Create PO"):
    response = requests.post(f"{API_URL}/purchase_orders/", json={"supplier_id": supplier_id, "items": items}, headers=headers)
    st.write(response.json())
