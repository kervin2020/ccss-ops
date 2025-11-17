'use client'

import { CustomButton } from './custom-button'
import { Card } from '@/components/ui/card'

export default function ButtonShowcase() {
  return (
    <div className="space-y-8 p-8">
      {/* Primary Buttons */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Primary Buttons</h2>
        <Card className="p-6 space-y-4">
          <div className="flex flex-wrap gap-4">
            <CustomButton variant="primary" size="sm">
              Small Button
            </CustomButton>
            <CustomButton variant="primary" size="md">
              Medium Button
            </CustomButton>
            <CustomButton variant="primary" size="lg">
              Large Button
            </CustomButton>
            <CustomButton variant="primary" disabled>
              Disabled Button
            </CustomButton>
          </div>
        </Card>
      </section>

      {/* Secondary Buttons */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Secondary Buttons</h2>
        <Card className="p-6 space-y-4">
          <div className="flex flex-wrap gap-4">
            <CustomButton variant="secondary" size="sm">
              Small Button
            </CustomButton>
            <CustomButton variant="secondary" size="md">
              Medium Button
            </CustomButton>
            <CustomButton variant="secondary" size="lg">
              Large Button
            </CustomButton>
            <CustomButton variant="secondary" disabled>
              Disabled Button
            </CustomButton>
          </div>
        </Card>
      </section>

      {/* Outline Buttons */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Outline Buttons</h2>
        <Card className="p-6 space-y-4">
          <div className="flex flex-wrap gap-4">
            <CustomButton variant="outline" size="sm">
              Small Button
            </CustomButton>
            <CustomButton variant="outline" size="md">
              Medium Button
            </CustomButton>
            <CustomButton variant="outline" size="lg">
              Large Button
            </CustomButton>
            <CustomButton variant="outline" disabled>
              Disabled Button
            </CustomButton>
          </div>
        </Card>
      </section>

      {/* Ghost Buttons */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Ghost Buttons</h2>
        <Card className="p-6 space-y-4">
          <div className="flex flex-wrap gap-4">
            <CustomButton variant="ghost" size="sm">
              Small Button
            </CustomButton>
            <CustomButton variant="ghost" size="md">
              Medium Button
            </CustomButton>
            <CustomButton variant="ghost" size="lg">
              Large Button
            </CustomButton>
            <CustomButton variant="ghost" disabled>
              Disabled Button
            </CustomButton>
          </div>
        </Card>
      </section>

      {/* Danger & Success Buttons */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Danger & Success Buttons</h2>
        <Card className="p-6 space-y-4">
          <div className="flex flex-wrap gap-4">
            <CustomButton variant="danger" size="md">
              Delete Account
            </CustomButton>
            <CustomButton variant="success" size="md">
              Save Changes
            </CustomButton>
            <CustomButton variant="danger" size="md" disabled>
              Delete (Disabled)
            </CustomButton>
            <CustomButton variant="success" size="md" disabled>
              Save (Disabled)
            </CustomButton>
          </div>
        </Card>
      </section>

      {/* Full Width & Loading */}
      <section>
        <h2 className="text-2xl font-bold mb-4">Full Width & Loading States</h2>
        <Card className="p-6 space-y-4">
          <CustomButton variant="primary" fullWidth size="md">
            Full Width Button
          </CustomButton>
          <CustomButton variant="secondary" fullWidth size="md" isLoading>
            Processing...
          </CustomButton>
        </Card>
      </section>
    </div>
  )
}
