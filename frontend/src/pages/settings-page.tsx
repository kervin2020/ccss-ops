import { Card } from '@/components/ui/card'
import { CustomButton } from '@/components/buttons/custom-button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-bold text-foreground">Settings</h2>
        <p className="text-sm text-muted-foreground mt-1">
          Manage your account and preferences.
        </p>
      </div>

      {/* Settings Sections */}
      <Card className="border-border/50 p-6">
        <h3 className="font-bold text-foreground mb-4">Account Settings</h3>
        <div className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="fullname" className="text-sm font-medium">
              Full Name
            </Label>
            <Input
              id="fullname"
              type="text"
              placeholder="John Doe"
              className="bg-input border-border/50"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email" className="text-sm font-medium">
              Email Address
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="john@example.com"
              className="bg-input border-border/50"
            />
          </div>
          <CustomButton variant="success" size="md">
            Save Changes
          </CustomButton>
        </div>
      </Card>

      {/* Preferences */}
      <Card className="border-border/50 p-6">
        <h3 className="font-bold text-foreground mb-4">Preferences</h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between py-3 border-b border-border/30">
            <span className="text-foreground">Email Notifications</span>
            <input type="checkbox" defaultChecked className="w-4 h-4" />
          </div>
          <div className="flex items-center justify-between py-3">
            <span className="text-foreground">Dark Mode</span>
            <input type="checkbox" defaultChecked className="w-4 h-4" />
          </div>
        </div>
      </Card>
    </div>
  )
}
