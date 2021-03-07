function formatMoney(number) {
  return parseFloat(number).toLocaleString("en-US", { style: "currency", currency: "USD" });
}
