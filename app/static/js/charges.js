function formatMoney(number) {
  return parseFloat(number).toLocaleString("en-US", { style: "currency", currency: "USD" });
}

function delete_bill(id, bldg_id) {
  if (confirm("Are you sure you want to delete Bill #" + id + "?")) {
    link = "/delete/" + id + "/" + bldg_id;
    window.location.replace(link);
  } else {
    console.log("delete action canceled");
  }
}

function edit(id, bldg_id) {
  var new_amount = prompt("Enter amount of new balance for Bill #" + id, 0);
  console.log(new_amount);
  if (new_amount != null) {
    if (confirm("Change balance for Bill #" + id + " to $" + new_amount + "?")) {
      link = "/edit/" + id + "/" + bldg_id + "/" + new_amount;
      window.location.replace(link);
    } else {
      console.log("edit action canceled");
    }
  }
}
