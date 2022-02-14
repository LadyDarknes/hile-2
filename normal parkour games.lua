local ScreenGui = Instance.new("ScreenGui")
local main = Instance.new("Frame")
local spdactivate = Instance.new("TextButton")
local jmpactivate = Instance.new("TextButton")
local spdtext = Instance.new("TextBox")
local X = Instance.new("TextButton")
local jmpdiss = Instance.new("TextButton")
local ac = Instance.new("TextButton")

ScreenGui.Parent = game.CoreGui

main.Name = "main"
main.Parent = ScreenGui
main.BackgroundColor3 = Color3.fromRGB(70, 39, 4)
main.Position = UDim2.new(0.243523329, 0, 0.226640165, 0)
main.Size = UDim2.new(0, 228, 0, 191)
main.Visible = false
main.Active = true
main.Draggable = true

spdactivate.Name = "spdactivate"
spdactivate.Parent = main
spdactivate.BackgroundColor3 = Color3.fromRGB(79, 238, 238)
spdactivate.Position = UDim2.new(0.540200949, 0, 0.111519352, 0)
spdactivate.Size = UDim2.new(0, 83, 0, 64)
spdactivate.Font = Enum.Font.SourceSans
spdactivate.Text = "Activate"
spdactivate.TextColor3 = Color3.fromRGB(0, 0, 0)
spdactivate.TextSize = 14.000
spdactivate.MouseButton1Down:connect(function()
	game.Players.LocalPlayer.Character.Humanoid.WalkSpeed = main.spdtext.Text
end)

jmpactivate.Name = "jmpactivate"
jmpactivate.Parent = main
jmpactivate.BackgroundColor3 = Color3.fromRGB(79, 238, 238)
jmpactivate.BorderColor3 = Color3.fromRGB(239, 239, 239)
jmpactivate.BorderSizePixel = 0
jmpactivate.Position = UDim2.new(0.540200889, 0, 0.603665948, 0)
jmpactivate.Size = UDim2.new(0, 83, 0, 64)
jmpactivate.Font = Enum.Font.SourceSans
jmpactivate.Text = "Activate"
jmpactivate.TextColor3 = Color3.fromRGB(0, 0, 0)
jmpactivate.TextSize = 14.000
jmpactivate.MouseButton1Down:connect(function()

	InfiniteJumpEnabled = true
	game:GetService("UserInputService").JumpRequest:connect(function()
		if InfiniteJumpEnabled then
			game:GetService"Players".LocalPlayer.Character:FindFirstChildOfClass'Humanoid':ChangeState("Jumping")
		end	
	end)
end)


spdtext.Name = "spdtext"
spdtext.Parent = main
spdtext.BackgroundColor3 = Color3.fromRGB(79, 238, 238)
spdtext.Position = UDim2.new(0.0622897893, 0, 0.110856727, 0)
spdtext.Size = UDim2.new(0, 79, 0, 64)
spdtext.Font = Enum.Font.SourceSans
spdtext.Text = "speed value"
spdtext.TextColor3 = Color3.fromRGB(0, 0, 0)
spdtext.TextSize = 14.000

X.Name = "X"
X.Parent = main
X.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
X.BackgroundTransparency = 1.000
X.BorderSizePixel = 0
X.Position = UDim2.new(0.903508782, 0, -0.0418848172, 0)
X.Size = UDim2.new(0, 28, 0, 29)
X.Font = Enum.Font.SourceSans
X.LineHeight = 1.130
X.Text = "X"
X.TextColor3 = Color3.fromRGB(0, 0, 0)
X.TextSize = 24.000
X.TextStrokeColor3 = Color3.fromRGB(63, 63, 63)
X.TextStrokeTransparency = 0.770
X.MouseButton1Down:connect(function()
	main.Visible = false
	ac.Visible = true
end)

jmpdiss.Name = "jmpdiss"
jmpdiss.Parent = main
jmpdiss.BackgroundColor3 = Color3.fromRGB(79, 238, 238)
jmpdiss.BorderColor3 = Color3.fromRGB(239, 239, 239)
jmpdiss.BorderSizePixel = 0
jmpdiss.Position = UDim2.new(0.0621307194, 0, 0.603665948, 0)
jmpdiss.Size = UDim2.new(0, 83, 0, 64)
jmpdiss.Font = Enum.Font.SourceSans
jmpdiss.Text = "dis jump"
jmpdiss.TextColor3 = Color3.fromRGB(0, 0, 0)
jmpdiss.TextSize = 14.000
jmpdiss.MouseButton1Down:connect(function()

	InfiniteJumpEnabled = false
	game:GetService("UserInputService").JumpRequest:connect(function()
		if InfiniteJumpEnabled then
			game:GetService"Players".LocalPlayer.Character:FindFirstChildOfClass'Humanoid':ChangeState("Jumping")
		end	
	end)
end)

ac.Name = "ac"
ac.Parent = ScreenGui
ac.BackgroundColor3 = Color3.fromRGB(248, 35, 255)
ac.Position = UDim2.new(0.52720207, 0, 0, 0)
ac.Size = UDim2.new(0, 79, 0, 50)
ac.Font = Enum.Font.SourceSans
ac.Text = "hileyi ac"
ac.TextColor3 = Color3.fromRGB(0, 0, 0)
ac.MouseButton1Down:connect(function()
ac.TextSize = 14.000
main.Visible = true
ac.Visible = false
end)
