local ScreenGui = Instance.new("ScreenGui")
local main = Instance.new("Frame")
local jumpon = Instance.new("TextButton")
local jumpoff = Instance.new("TextButton")
local hzon = Instance.new("TextButton")
local hzoff = Instance.new("TextButton")
local kapa = Instance.new("TextButton")

ScreenGui.Parent = game.CoreGui

main.Name = "main"
main.Parent = ScreenGui
main.BackgroundColor3 = Color3.fromRGB(175, 175, 175)
main.Position = UDim2.new(0.540342331, 0, 0.284294248, 0)
main.Size = UDim2.new(0, 298, 0, 217)
main.Active = true
main.Draggable = true

jumpon.Name = "jumpon"
jumpon.Parent = main
jumpon.BackgroundColor3 = Color3.fromRGB(90, 90, 90)
jumpon.Position = UDim2.new(0, 0, 0.769585252, 0)
jumpon.Size = UDim2.new(0, 156, 0, 50)
jumpon.Font = Enum.Font.SourceSans
jumpon.Text = "Sonsuz zıplama aç"
jumpon.TextColor3 = Color3.fromRGB(0, 0, 0)
jumpon.TextSize = 14.000
jumpon.MouseButton1Down:connect(function()
	
	InfiniteJumpEnabled = true
	game:GetService("UserInputService").JumpRequest:connect(function()
		if InfiniteJumpEnabled then
			game:GetService"Players".LocalPlayer.Character:FindFirstChildOfClass'Humanoid':ChangeState("Jumping")
		end	
     end)
end)

jumpoff.Name = "jumpoff"
jumpoff.Parent = main
jumpoff.BackgroundColor3 = Color3.fromRGB(90, 90, 90)
jumpoff.Position = UDim2.new(0.523489952, 0, 0.769585252, 0)
jumpoff.Size = UDim2.new(0, 142, 0, 50)
jumpoff.Font = Enum.Font.SourceSans
jumpoff.Text = "Sonsuz zıplama kapa"
jumpoff.TextColor3 = Color3.fromRGB(0, 0, 0)
jumpoff.TextSize = 14.000
jumpoff.MouseButton1Down:connect(function()

	InfiniteJumpEnabled = false
	game:GetService("UserInputService").JumpRequest:connect(function()
		if InfiniteJumpEnabled then
			game:GetService"Players".LocalPlayer.Character:FindFirstChildOfClass'Humanoid':ChangeState("Jumping")
		end	
	end)
end)


hzon.Name = "hızon"
hzon.Parent = main
hzon.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
hzon.Position = UDim2.new(0, 0, 0.539170504, 0)
hzon.Size = UDim2.new(0, 156, 0, 50)
hzon.Font = Enum.Font.SourceSans
hzon.Text = "hızı aç"
hzon.TextColor3 = Color3.fromRGB(0, 0, 0)
hzon.TextSize = 14.000
hzon.MouseButton1Down:connect(function()
	game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = 20
end)

hzoff.Name = "hızoff"
hzoff.Parent = main
hzoff.BackgroundColor3 = Color3.fromRGB(50, 50, 50)
hzoff.Position = UDim2.new(0.523489952, 0, 0.539170504, 0)
hzoff.Size = UDim2.new(0, 142, 0, 50)
hzoff.Font = Enum.Font.SourceSans
hzoff.Text = "hızı kapa"
hzoff.TextColor3 = Color3.fromRGB(0, 0, 0)
hzoff.TextSize = 14.000
hzoff.MouseButton1Down:connect(function()
	game.Players.LocalPlayer.Character.Humanoid.WalkSpeed =  30
end)

kapa.Name = "kapa"
kapa.Parent = main
kapa.BackgroundColor3 = Color3.fromRGB(90, 90, 90)
kapa.Position = UDim2.new(0, 0, 0.308755755, 0)
kapa.Size = UDim2.new(0, 298, 0, 50)
kapa.Font = Enum.Font.SourceSans
kapa.Text = "menüyü kapat!"
kapa.TextColor3 = Color3.fromRGB(0, 0, 0)
kapa.TextSize = 14.000
kapa.MouseButton1Down:connect(function()
	main.Visible = not main.Visible;
end)
