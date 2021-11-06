local ScreenGui = Instance.new("ScreenGui")
local main = Instance.new("Frame")
local aktif = Instance.new("TextButton")
local kapat = Instance.new("TextButton")
local label = Instance.new("TextLabel")

ScreenGui.Parent = game.CoreGui

main.Name = "main"
main.Parent = ScreenGui
main.BackgroundColor3 = Color3.fromRGB(175, 175, 175)
main.Position = UDim2.new(0.438875318, 0, 0.238568589, 0)
main.Size = UDim2.new(0, 258, 0, 180)
main.Active = true
main.Draggable = true

aktif.Name = "aktif"
aktif.Parent = main
aktif.BackgroundColor3 = Color3.fromRGB(175, 175, 175)
aktif.Size = UDim2.new(0, 258, 0, 53)
aktif.Font = Enum.Font.SourceSans
aktif.Text = "hileyi aç!"
aktif.TextColor3 = Color3.fromRGB(0, 0, 0)
aktif.TextSize = 14.000
aktif.MouseButton1Down:connect(function()
	loadstring(game:HttpGet("https://raw.githubusercontent.com/aniltosun29/hile-2/main/be%20a%20parkour%20ninja%20script.lua"))()
end)

kapat.Name = "kapat"
kapat.Parent = main
kapat.BackgroundColor3 = Color3.fromRGB(175, 175, 175)
kapat.Position = UDim2.new(0, 0, 0.705555558, 0)
kapat.Size = UDim2.new(0, 258, 0, 53)
kapat.Font = Enum.Font.SourceSans
kapat.Text = "Menüyü kapat!"
kapat.TextColor3 = Color3.fromRGB(0, 0, 0)
kapat.TextSize = 14.000
kapat.MouseButton1Click:Connect(function()
       main.Visible = not main.Visible;
end)

label.Name = "label"
label.Parent = main
label.BackgroundColor3 = Color3.fromRGB(175, 175, 175)
label.Position = UDim2.new(0, 0, 0.294444442, 0)
label.Size = UDim2.new(0, 258, 0, 74)
label.Font = Enum.Font.SourceSans
label.Text = "parkour ninja hack"
label.TextColor3 = Color3.fromRGB(0, 0, 0)
label.TextSize = 14.000
