# po_lifecycle.py
st.title("📑 Purchase Order Lifecycle Management")

po_id = st.number_input("PO ID", min_value=1)
new_status = st.selectbox("Update Status", ["Draft", "Sent", "Confirmed", "Delivered", "Closed"])

if st.button("Update PO Status"):
    response = requests.post(f"{API_URL}/purchase_orders/{po_id}/update_status/", 
                             params={"new_status": new_status}, headers=headers)
    st.write(response.json())
