resource "azurerm_storage_account" "insecure_example" {
  name                     = "insecurestorageexample"
  resource_group_name      = "rg-example"
  location                 = "westeurope"
  account_tier             = "Standard"
  account_replication_type = "LRS"

  allow_nested_items_to_be_public = false
  min_tls_version                 = "TLS1_2"

  network_rules {
    default_action = "Deny"
  }
}