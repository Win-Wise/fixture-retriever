#define variables
locals {
  layer_zip_name    = "lambda_layer.zip"
  layer_name        = "arbriver_python_layer"
  requirements_name = filesha1("base/target/${local.layer_zip_name}")
}

# define existing bucket for storing lambda layers
resource "aws_s3_bucket" "lambda_layer" {
  bucket_prefix = "arbriver-python-layer"
}

# upload zip file to s3
resource "aws_s3_object" "lambda_layer_zip" {
  bucket     = aws_s3_bucket.lambda_layer.id
  key        = "lambda_layers/${local.layer_name}/layer-${local.requirements_name}"
  source     = "base/target/${local.layer_zip_name}"
}

# create lambda layer from s3 object
resource "aws_lambda_layer_version" "lambda_layer" {
  s3_bucket           = aws_s3_bucket.lambda_layer.id
  s3_key              = aws_s3_object.lambda_layer_zip.key
  layer_name          = local.layer_name
  compatible_runtimes = ["python3.11"]
  skip_destroy        = true
  depends_on          = [aws_s3_object.lambda_layer_zip] # triggered only if the zip file is uploaded to the bucket
}