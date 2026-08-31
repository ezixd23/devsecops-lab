resource "local_file" "lab_info" {
  filename = "${path.module}/lab-info.txt"
  content  = "DevSecOps Lab — environment: ${var.environment}\n"
}