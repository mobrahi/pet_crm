# suppliers.py
st.title("🤝 Supplier Management")

# Add supplier
st.header("Add Supplier")
sup_name = st.text_input("Supplier Name")
sup_email = st.text_input("Contact Email")
sup_phone = st.text_input("Phone")
if st.button("Add Supplier"):
    response = requests.post(f"{API_URL}/suppliers/", params={
        "name": sup_name, "contact_email": sup_email, "phone": sup_phone
    }, headers=headers)
    st.write(response.json())

# Reorder requests
st.header("Reorder Requests")
response = requests.get(f"{API_URL}/reports/reorder_requests/", headers=headers)
data = pd.DataFrame(response.json())
if not data.empty:
    st.table(data)
else:
    st.write("✅ No products need reordering right now")
