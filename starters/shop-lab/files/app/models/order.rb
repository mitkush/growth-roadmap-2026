class Order < ApplicationRecord
  STATUSES = %w[pending paid shipped refunded].freeze

  belongs_to :customer
  has_many :line_items
  has_many :products, through: :line_items
end
