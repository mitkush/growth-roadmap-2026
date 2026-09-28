# Deliberately slow for Step 1: loads 50k rows as Ruby objects and aggregates in Ruby,
# allocating many intermediate arrays and strings. Profile it, then make it fast.
class ReportsController < ApplicationController
  def sales
    line_items = LineItem.includes(:product).where(id: ..50_000).to_a
    report = line_items.group_by { |item| item.product.category }.map do |category, items|
      revenue_cents = items.map { |item| item.quantity * item.unit_price_cents }.sum
      top_skus = items.map { |item| item.product.sku }.tally.sort_by { |sku, count| [-count, sku] }.first(3).map(&:first) # ties: by SKU
      { category: category, items: items.size, revenue: format("%.2f", revenue_cents / 100.0), top_skus: top_skus }
    end
    render json: report.sort_by { |row| row[:category] }
  end
end
