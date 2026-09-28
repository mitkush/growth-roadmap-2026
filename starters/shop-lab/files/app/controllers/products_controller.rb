# Deliberately naive for Steps 1-2: one extra query per product (N+1).
class ProductsController < ApplicationController
  def index
    products = Product.order(:id).limit(100)
    render json: products.map { |product|
      {
        id: product.id, name: product.name, sku: product.sku, price_cents: product.price_cents,
        units_sold: product.line_items.sum(:quantity) # N+1: a SUM query for every product
      }
    }
  end
end
