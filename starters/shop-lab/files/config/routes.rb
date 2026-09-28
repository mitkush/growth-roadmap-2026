Rails.application.routes.draw do
  get "up" => "rails/health#show", as: :rails_health_check

  resources :products, only: :index
  get "reports/sales", to: "reports#sales"
  get "slow_io", to: "slow_io#show"
end
