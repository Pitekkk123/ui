import { jsPDF } from "jspdf"

interface InvoiceItem {
  item: string
  qty: number
  unitPrice: number
}

interface InvoiceData {
  invoiceNumber: string
  dueDate: string
  status: string
  companyName: string
  companyAddress: string[]
  clientName: string
  clientAddress: string[]
  items: InvoiceItem[]
  taxRate: number
  notes?: string
  paymentTerms?: string
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(value)
}

export function generatePremiumPdf(data: InvoiceData) {
  const doc = new jsPDF({
    orientation: "portrait",
    unit: "mm",
    format: "a4",
  })

  const pageWidth = doc.internal.pageSize.getWidth()
  const pageHeight = doc.internal.pageSize.getHeight()
  const margin = 20
  const contentWidth = pageWidth - margin * 2

  // --- Colors ---
  const primaryColor: [number, number, number] = [15, 23, 42] // slate-900
  const accentColor: [number, number, number] = [99, 102, 241] // indigo-500
  const mutedColor: [number, number, number] = [100, 116, 139] // slate-500
  const lightBg: [number, number, number] = [248, 250, 252] // slate-50
  const borderColor: [number, number, number] = [226, 232, 240] // slate-200
  const white: [number, number, number] = [255, 255, 255]

  let y = 0

  // ===== TOP ACCENT BAR =====
  doc.setFillColor(...accentColor)
  doc.rect(0, 0, pageWidth, 4, "F")

  y = 20

  // ===== HEADER =====
  // Company name (left)
  doc.setFont("helvetica", "bold")
  doc.setFontSize(22)
  doc.setTextColor(...primaryColor)
  doc.text(data.companyName, margin, y)

  // INVOICE label (right)
  doc.setFont("helvetica", "bold")
  doc.setFontSize(28)
  doc.setTextColor(...accentColor)
  doc.text("INVOICE", pageWidth - margin, y, { align: "right" })

  y += 8

  // Company address
  doc.setFont("helvetica", "normal")
  doc.setFontSize(9)
  doc.setTextColor(...mutedColor)
  for (const line of data.companyAddress) {
    doc.text(line, margin, y)
    y += 4
  }

  y += 8

  // ===== INVOICE INFO BOX =====
  const infoBoxY = y
  const infoBoxHeight = 28

  doc.setFillColor(...lightBg)
  doc.roundedRect(margin, infoBoxY, contentWidth, infoBoxHeight, 3, 3, "F")

  doc.setDrawColor(...borderColor)
  doc.setLineWidth(0.3)
  doc.roundedRect(margin, infoBoxY, contentWidth, infoBoxHeight, 3, 3, "S")

  const infoY = infoBoxY + 10
  const col1 = margin + 8
  const col2 = margin + contentWidth * 0.25
  const col3 = margin + contentWidth * 0.5
  const col4 = margin + contentWidth * 0.75

  // Labels
  doc.setFont("helvetica", "normal")
  doc.setFontSize(7)
  doc.setTextColor(...mutedColor)
  doc.text("INVOICE NUMBER", col1, infoY)
  doc.text("ISSUE DATE", col2, infoY)
  doc.text("DUE DATE", col3, infoY)
  doc.text("STATUS", col4, infoY)

  // Values
  doc.setFont("helvetica", "bold")
  doc.setFontSize(10)
  doc.setTextColor(...primaryColor)
  doc.text(data.invoiceNumber, col1, infoY + 7)

  const today = new Date().toLocaleDateString("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  })
  doc.text(today, col2, infoY + 7)
  doc.text(data.dueDate, col3, infoY + 7)

  // Status badge
  const statusX = col4
  const statusY = infoY + 3
  const statusWidth = 22
  const statusHeight = 7

  if (data.status === "Pending") {
    doc.setFillColor(254, 243, 199) // amber-100
    doc.roundedRect(statusX - 1, statusY, statusWidth, statusHeight, 2, 2, "F")
    doc.setFontSize(7)
    doc.setFont("helvetica", "bold")
    doc.setTextColor(180, 83, 9) // amber-700
  } else if (data.status === "Paid") {
    doc.setFillColor(209, 250, 229) // emerald-100
    doc.roundedRect(statusX - 1, statusY, statusWidth, statusHeight, 2, 2, "F")
    doc.setFontSize(7)
    doc.setFont("helvetica", "bold")
    doc.setTextColor(4, 120, 87) // emerald-700
  } else {
    doc.setFillColor(224, 231, 255) // indigo-100
    doc.roundedRect(statusX - 1, statusY, statusWidth, statusHeight, 2, 2, "F")
    doc.setFontSize(7)
    doc.setFont("helvetica", "bold")
    doc.setTextColor(67, 56, 202) // indigo-700
  }
  doc.text(data.status.toUpperCase(), statusX + statusWidth / 2 - 1, statusY + 5, {
    align: "center",
  })

  y = infoBoxY + infoBoxHeight + 14

  // ===== BILL TO =====
  doc.setFont("helvetica", "normal")
  doc.setFontSize(7)
  doc.setTextColor(...mutedColor)
  doc.text("BILL TO", margin, y)
  y += 6

  doc.setFont("helvetica", "bold")
  doc.setFontSize(11)
  doc.setTextColor(...primaryColor)
  doc.text(data.clientName, margin, y)
  y += 5

  doc.setFont("helvetica", "normal")
  doc.setFontSize(9)
  doc.setTextColor(...mutedColor)
  for (const line of data.clientAddress) {
    doc.text(line, margin, y)
    y += 4
  }

  y += 10

  // ===== TABLE =====
  const tableStartY = y
  const colWidths = [contentWidth * 0.45, contentWidth * 0.12, contentWidth * 0.2, contentWidth * 0.23]
  const colStarts = [
    margin,
    margin + colWidths[0],
    margin + colWidths[0] + colWidths[1],
    margin + colWidths[0] + colWidths[1] + colWidths[2],
  ]

  // Table header
  const headerHeight = 12
  doc.setFillColor(...primaryColor)
  doc.roundedRect(margin, y, contentWidth, headerHeight, 2, 2, "F")
  // Cover bottom corners with a filled rect so only top is rounded
  doc.rect(margin, y + 6, contentWidth, 6, "F")

  doc.setFont("helvetica", "bold")
  doc.setFontSize(8)
  doc.setTextColor(...white)

  const headerY = y + 8
  doc.text("ITEM DESCRIPTION", colStarts[0] + 6, headerY)
  doc.text("QTY", colStarts[1] + colWidths[1] / 2, headerY, { align: "center" })
  doc.text("UNIT PRICE", colStarts[2] + colWidths[2] - 4, headerY, { align: "right" })
  doc.text("AMOUNT", colStarts[3] + colWidths[3] - 6, headerY, { align: "right" })

  y += headerHeight

  // Table rows
  const rowHeight = 12
  doc.setFontSize(9)

  for (let i = 0; i < data.items.length; i++) {
    const row = data.items[i]
    const amount = row.qty * row.unitPrice

    // Alternate row background
    if (i % 2 === 0) {
      doc.setFillColor(...lightBg)
      doc.rect(margin, y, contentWidth, rowHeight, "F")
    }

    // Bottom border
    doc.setDrawColor(...borderColor)
    doc.setLineWidth(0.2)
    doc.line(margin, y + rowHeight, margin + contentWidth, y + rowHeight)

    const rowTextY = y + 8

    doc.setFont("helvetica", "normal")
    doc.setTextColor(...primaryColor)
    doc.text(row.item, colStarts[0] + 6, rowTextY)

    doc.setTextColor(...mutedColor)
    doc.text(String(row.qty), colStarts[1] + colWidths[1] / 2, rowTextY, { align: "center" })

    doc.text(formatCurrency(row.unitPrice), colStarts[2] + colWidths[2] - 4, rowTextY, {
      align: "right",
    })

    doc.setFont("helvetica", "bold")
    doc.setTextColor(...primaryColor)
    doc.text(formatCurrency(amount), colStarts[3] + colWidths[3] - 6, rowTextY, {
      align: "right",
    })

    y += rowHeight
  }

  y += 4

  // ===== TOTALS =====
  const totalsX = colStarts[2]
  const totalsValueX = colStarts[3] + colWidths[3] - 6

  const subtotal = data.items.reduce((sum, row) => sum + row.qty * row.unitPrice, 0)
  const tax = subtotal * data.taxRate
  const totalDue = subtotal + tax

  // Subtotal
  doc.setFont("helvetica", "normal")
  doc.setFontSize(9)
  doc.setTextColor(...mutedColor)
  doc.text("Subtotal", totalsX, y + 6)
  doc.setTextColor(...primaryColor)
  doc.text(formatCurrency(subtotal), totalsValueX, y + 6, { align: "right" })

  y += 10

  // Tax
  doc.setTextColor(...mutedColor)
  doc.text(`Tax (${(data.taxRate * 100).toFixed(0)}%)`, totalsX, y + 6)
  doc.setTextColor(...primaryColor)
  doc.text(formatCurrency(tax), totalsValueX, y + 6, { align: "right" })

  y += 10

  // Separator
  doc.setDrawColor(...borderColor)
  doc.setLineWidth(0.3)
  doc.line(totalsX, y + 2, totalsValueX + 2, y + 2)

  y += 6

  // Total Due - highlighted box
  const totalBoxWidth = totalsValueX - totalsX + 8
  doc.setFillColor(...accentColor)
  doc.roundedRect(totalsX - 4, y, totalBoxWidth, 14, 3, 3, "F")

  doc.setFont("helvetica", "bold")
  doc.setFontSize(10)
  doc.setTextColor(...white)
  doc.text("TOTAL DUE", totalsX + 2, y + 9)
  doc.setFontSize(13)
  doc.text(formatCurrency(totalDue), totalsValueX, y + 9.5, { align: "right" })

  y += 26

  // ===== NOTES & PAYMENT TERMS =====
  if (data.notes || data.paymentTerms) {
    // Divider
    doc.setDrawColor(...borderColor)
    doc.setLineWidth(0.3)
    doc.line(margin, y, margin + contentWidth, y)
    y += 8

    if (data.paymentTerms) {
      doc.setFont("helvetica", "bold")
      doc.setFontSize(8)
      doc.setTextColor(...primaryColor)
      doc.text("PAYMENT TERMS", margin, y)
      y += 5

      doc.setFont("helvetica", "normal")
      doc.setFontSize(9)
      doc.setTextColor(...mutedColor)
      doc.text(data.paymentTerms, margin, y)
      y += 8
    }

    if (data.notes) {
      doc.setFont("helvetica", "bold")
      doc.setFontSize(8)
      doc.setTextColor(...primaryColor)
      doc.text("NOTES", margin, y)
      y += 5

      doc.setFont("helvetica", "normal")
      doc.setFontSize(9)
      doc.setTextColor(...mutedColor)
      const noteLines = doc.splitTextToSize(data.notes, contentWidth)
      doc.text(noteLines, margin, y)
      y += noteLines.length * 4 + 4
    }
  }

  // ===== FOOTER =====
  const footerY = pageHeight - 16

  // Footer accent line
  doc.setDrawColor(...accentColor)
  doc.setLineWidth(0.5)
  doc.line(margin, footerY - 4, margin + contentWidth, footerY - 4)

  doc.setFont("helvetica", "normal")
  doc.setFontSize(7)
  doc.setTextColor(...mutedColor)
  doc.text(
    "Thank you for your business. This invoice was generated automatically.",
    margin,
    footerY
  )

  doc.setTextColor(...accentColor)
  doc.text("PREMIUM", pageWidth - margin, footerY, { align: "right" })

  // Bottom accent bar
  doc.setFillColor(...accentColor)
  doc.rect(0, pageHeight - 4, pageWidth, 4, "F")

  // Save
  doc.save(`${data.invoiceNumber}-premium.pdf`)
}

export const DEFAULT_INVOICE_DATA: InvoiceData = {
  invoiceNumber: "INV-2847",
  dueDate: "March 30, 2026",
  status: "Pending",
  companyName: "Acme Design Co.",
  companyAddress: [
    "1234 Innovation Drive, Suite 500",
    "San Francisco, CA 94105",
    "hello@acmedesign.co",
  ],
  clientName: "Stark Industries",
  clientAddress: [
    "200 Park Avenue",
    "New York, NY 10166",
    "accounts@starkindustries.com",
  ],
  items: [
    { item: "Design System License", qty: 1, unitPrice: 499 },
    { item: "Priority Support (12 months)", qty: 12, unitPrice: 99 },
    { item: "Custom Components", qty: 3, unitPrice: 250 },
  ],
  taxRate: 0,
  paymentTerms: "Net 30 — Payment due within 30 days of invoice date.",
  notes:
    "This invoice includes a Design System License for unlimited team members, 12 months of priority support with 24h response time, and 3 custom-built components tailored to your brand guidelines.",
}
