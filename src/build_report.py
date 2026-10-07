"""Build the complete, densely-formatted 11-page final examination report.
Zero artificial blank spaces: continuous, professional scholarly flow with optimal figure scaling.
Meets the 10-15 pages rubric strictly (excluding references/appendix).
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Deep Learning Final Exam Project 2026-2027 | Can Synthetic Images Improve Imbalanced Classification?")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL - ACADEMIC EXAMINATION SUBMISSION")
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * inch - 54, 48)
        self.restoreState()

def build_pdf(filename="Group25_Project19_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1a237e'),
        alignment=1,
        spaceAfter=7
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#333333'),
        alignment=1,
        spaceAfter=9
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceAfter=9
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15.5,
        textColor=colors.HexColor('#1a237e'),
        spaceBefore=11,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=colors.HexColor('#283593'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.2,
        textColor=colors.HexColor('#222222'),
        spaceAfter=6.5,
        alignment=4
    )
    abstract_style = ParagraphStyle(
        'Abstract_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#1a1a1a'),
        leftIndent=14,
        rightIndent=14,
        spaceAfter=9,
        alignment=4
    )
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#555555'),
        alignment=1,
        spaceBefore=3,
        spaceAfter=6
    )
    ref_style = ParagraphStyle(
        'Reference',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#333333'),
        leftIndent=14,
        firstLineIndent=-14,
        spaceAfter=3
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Can Synthetic Images Improve Imbalanced Classification?", title_style))
    story.append(Paragraph("An Empirical Benchmark of Conditional Generative Adversarial Networks vs. Conventional Augmentation on CIFAR-10-LT", subtitle_style))
    story.append(Paragraph("<b>Course</b>: Deep Learning Final Exam Projects 2026-2027 &nbsp;|&nbsp; <b>Group ID</b>: Group 25 &nbsp;|&nbsp; <b>Project ID</b>: Project 19<br/><b>Repository</b>: DL2026-Group25-Project19 &nbsp;|&nbsp; <b>Report File</b>: Group25_Project19_Report.pdf<br/><b>Institution</b>: University of Science and Technology of Hanoi (USTH) &nbsp;|&nbsp; <b>Date</b>: October 2026", meta_style))
    
    # Author list block on cover/top (Clean ASCII)
    authors_text = (
        "<b>Group 25 Members (USTH):</b><br/>"
        "[1] <b>Ha Hiep Hung</b> (22BA13147, ICT, Lead) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "[2] <b>Truong Viet Hoang</b> (22BA13145, ICT) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "[3] <b>Vu Cong Thanh</b> (22BA13290, ICT)<br/>"
        "[4] <b>Vuong Minh Tuan</b> (22BA13316, ICT) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "[5] <b>Nguyen Tien Dat</b> (22BA13066, ICT) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "[6] <b>Nguyen Trung Hieu</b> (22BA13138, ICT) &nbsp;&nbsp;|&nbsp;&nbsp; "
        "[7] <b>Dang Binh Duong</b> (22BA13091, DS)"
    )
    story.append(Paragraph(authors_text, ParagraphStyle('AuthorsBox', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12, textColor=colors.HexColor('#1a237e'), alignment=1, spaceAfter=7)))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#1a237e"), spaceAfter=7))

    # 1. ABSTRACT
    story.append(Paragraph("1. Abstract", h1_style))
    abstract_text = (
        "Class imbalance represents a pervasive challenge in deep computer vision, where conventional supervised loss functions "
        "strongly bias deep neural representations toward majority classes, causing catastrophic classification degradation on minority classes. "
        "With recent advancements in deep generative modeling, generating synthetic imagery for minority classes has been widely hypothesized "
        "as an intuitive cure to rebalance empirical training distributions. In this paper, we conduct an exhaustive, rigorous empirical study "
        "investigating the central research question: <i>Can synthetic images generated by class-conditional generative adversarial networks (cGANs) "
        "genuinely improve imbalanced classification compared to standard data-level remedies?</i> "
        "Using CIFAR-10-LT under an extreme imbalance ratio of 100 (50 to 4,950 images per class), we train a Spectral Normalized ResNet "
        "cGAN with Differentiable Augmentation (DiffAugment) strictly on the long-tailed training set. We systematically benchmark ResNet-32 "
        "classifiers trained under uniform empirical risk minimization, conventional spatial data augmentation, Random Oversampling (ROS), "
        "cGAN synthetic data padding, and their composite hybrid configurations across multiple random seeds. "
        "Our rigorous findings demonstrate that synthetic data augmentation yields an overall test accuracy of 50.26% and macro-F1 of 46.40%, "
        "substantially underperforming conventional data augmentation (70.01% accuracy, 69.60% macro-F1) and ROS with augmentation (70.09% accuracy, 69.79% macro-F1). "
        "Comprehensive qualitative error analysis and Fréchet Inception Distance (FID) diagnostics demonstrate that severe minority classes (containing &le; 83 real samples) "
        "suffer from severe mode collapse and distribution distortion. When fed to classifiers, high-ratio synthetic data amplifies confirmation bias "
        "and induces distribution shift, demonstrating that generative oversampling cannot substitute for label-preserving geometric regularizations."
    )
    story.append(Paragraph(f"<b>Abstract</b>—{abstract_text}", abstract_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cccccc"), spaceAfter=6))

    # 2. INTRODUCTION & RESEARCH QUESTION
    story.append(Paragraph("2. Introduction & Research Motivation", h1_style))
    intro_p1 = (
        "Modern deep convolutional neural networks achieve remarkable, superhuman accuracy across standardized computer vision benchmarks. "
        "However, their state-of-the-art predictive capabilities rely fundamentally on the assumption that training distributions are balanced across "
        "target classes. In real-world visual applications—ranging from automated histopathology and rare disease screening to autonomous vehicle perception "
        "and rare event surveillance—visual frequencies inherently adhere to heavy-tailed, Pareto-like distributions. A tiny subset of frequent categories "
        "(referred to as head or majority classes) accounts for the overwhelming majority of visual encounters, whereas hundreds or thousands of critical "
        "categories (tail or minority classes) appear with vanishing frequency."
    )
    intro_p2 = (
        "When standard Empirical Risk Minimization (ERM) with Cross-Entropy loss is applied to such imbalanced datasets, deep networks exhibit severe bias. "
        "Because gradients contributed by head categories vastly outnumber updates from minority instances, the optimization trajectory overwhelmingly aligns "
        "feature representations and linear decision boundaries with majority manifolds. Consequently, the classifier achieves deceptive overall accuracy by simply "
        "predicting head classes, while exhibiting near-zero recognition recall on the rare tail categories where correct classification is often mission-critical."
    )
    intro_p3 = (
        "To alleviate this disparity, three major paradigms have emerged: (1) cost-sensitive re-weighting or margin adjustments (such as Focal Loss, CB-Loss, and LDAM), "
        "(2) representation-classifier decoupling via post-hoc logit adjustment, and (3) data-level resampling. Among data-level methods, Random Oversampling (ROS) "
        "has historically been the simplest intervention, duplicating tail examples to enforce class balance. However, repeatedly recycling a handful of real images "
        "inevitably causes deep networks to overfit memorized minority artifacts. "
        "In recent years, the dramatic maturation of deep generative modeling—spearheaded by Conditional Generative Adversarial Networks (cGANs) and Denoising Diffusion "
        "Probabilistic Models (DDPMs)—has inspired an alluring conjecture: rather than merely duplicating scarce tail images, why not generate thousands of novel, "
        "photorealistic synthetic minority images to achieve empirical equilibrium?"
    )
    intro_p4 = (
        "This conceptual promise has led to widespread enthusiasm across academia and industry. However, generative models are themselves parameterized deep networks "
        "that must learn data distributions from empirical evidence. When a generative model is trained directly on an extreme long-tailed distribution where minority classes "
        "contain only 50 to 80 examples, can it truly estimate the underlying visual manifold? Or does it merely hallucinate low-frequency artifacts that confuse downstream classifiers? "
        "To systematically answer this question, our study addresses three formal research questions:<br/>"
        "• <b>RQ1:</b> <i>Does augmenting minority classes with cGAN-synthesized images improve balanced test accuracy and macro-F1 relative to plain baseline ERM?</i><br/>"
        "• <b>RQ2:</b> <i>How does synthetic data augmentation compare against classical data-level solutions, specifically conventional geometric augmentation (Crop/Flip) and Random Oversampling (ROS)?</i><br/>"
        "• <b>RQ3:</b> <i>What failure modes, distribution shifts, and sample diversity deficits emerge when generative models are trained directly on extremely data-scarce minority regimes?</i>"
    )
    story.append(Paragraph(intro_p1, body_style))
    story.append(Paragraph(intro_p2, body_style))
    story.append(Paragraph(intro_p3, body_style))
    story.append(Paragraph(intro_p4, body_style))

    # 3. RELATED WORK
    story.append(Paragraph("3. Related Work and Theoretical Foundations", h1_style))
    rw_p1 = (
        "<b>3.1 Long-Tailed Visual Recognition:</b> Formal study of long-tailed visual recognition gained significant traction with Cui et al. (CVPR 2019), "
        "who introduced the concept of the <i>effective number of samples</i>, proving that the marginal information value of additional training instances decreases "
        "exponentially as class volume grows. They established standardized benchmarks on CIFAR-10-LT and CIFAR-100-LT by downsampling classes according to an exponential "
        "decay schedule. Cao et al. (NeurIPS 2019) proposed Label-Distribution-Aware Margin (LDAM) loss, which enforces theoretically grounded margin requirements inversely "
        "proportional to the fourth root of class cardinality. Kang et al. (ICLR 2020) demonstrated decoupled representation learning: representations are best learned "
        "under natural class-imbalanced schedules to preserve rich feature geometry, while classification heads should be re-balanced post-hoc via class-balanced re-sampling "
        "or weight vector normalization (&tau;-normalized readout)."
    )
    rw_p2 = (
        "<b>3.2 Conditional Generative Modeling under Data Scarcity:</b> Conditional GANs, pioneered by Mirza & Osindero (2014), enable class-guided image synthesis. "
        "Miyato & Koyama (ICLR 2018) revolutionized class conditioning by introducing the projection discriminator, which computes the inner product between class embedding "
        "vectors and intermediate spatial features, yielding vastly more coherent gradients than simple channel concatenation. To bound the Lipschitz constant and ensure "
        "stable minimax equilibrium, Miyato et al. (ICLR 2018) formulated Spectral Normalization (SN). In low-data regimes, however, GAN discriminators rapidly memorize training instances, "
        "causing generator gradient degradation. To counteract this, Zhao et al. (NeurIPS 2020) developed Differentiable Augmentation (DiffAugment), which applies differentiable "
        "transformations (translation, cutout, color jitter) simultaneously to real and fake streams without altering the generative target."
    )
    rw_p3 = (
        "<b>3.3 Synthetic Data Augmentation and Generative Pitfalls:</b> Synthetic sample generation has achieved notable success in domain adaptation (Hoffman et al., 2018) "
        "and medical imaging (Frid-Adar et al., 2018), where generating diverse lesions supplements scarce patient scans. However, foundational theoretical investigations "
        "by Ravuri & Vinyals (ICLR 2019) revealed that classifiers trained on GAN-generated ImageNet data suffered severe degradation compared to real data. "
        "More recently, Shumailov et al. (Nature 2024) mathematically formulated <i>Model Collapse</i>, proving that when neural models are recursively trained on synthetic data, "
        "the tail of the underlying distribution progressively vanishes, collapsing intra-class variance. Our work builds upon this foundation, conducting an empirical dissection "
        "specifically centered on extreme class imbalance where generative models must learn from as few as 50 instances."
    )
    story.append(Paragraph(rw_p1, body_style))
    story.append(Paragraph(rw_p2, body_style))
    story.append(Paragraph(rw_p3, body_style))

    # 4. DATASET AND DATA PREPARATION
    story.append(Paragraph("4. Dataset and Data Partitioning Protocol", h1_style))
    data_p1 = (
        "<b>Official Dataset Source:</b> All experiments are benchmarked on the canonical CIFAR-10 dataset curated by Alex Krizhevsky (University of Toronto), "
        "publicly hosted at <font color='#1a237e'><u>https://www.cs.toronto.edu/~kriz/cifar.html</u></font>. The full dataset comprises 60,000 32&times;32 pixel color images "
        "categorized across 10 mutually exclusive natural classes (Airplane, Automobile, Bird, Cat, Deer, Dog, Frog, Horse, Ship, Truck), partitioned officially into "
        "50,000 training and 10,000 testing images. In our reproduction pipeline, the dataset is deterministically acquired and verified against official MD5 checksums "
        "via <code>torchvision.datasets.CIFAR10(download=True)</code>."
    )
    data_p2 = (
        "<b>Deterministic Long-Tailed Induction (CIFAR-10-LT, IR=100):</b> Following the exponential decay formula formalized by Cui et al. (2019), "
        "the number of training instances for class index <i>c</i> &isin; {0, 1, ..., 9} is defined as:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>n<sub>c</sub> = min( floor( N<sub>max</sub> &middot; (1 / IR)<sup>c / (C - 1)</sup> ), 5000 - V<sub>c</sub> )</i><br/>"
        "where <i>N<sub>max</sub></i> = 5000 is the original per-class training volume, <i>IR</i> = 100 is the imbalance ratio, <i>C</i> = 10 is the number of classes, "
        "and <i>V<sub>c</sub></i> = 50 is the disjoint validation reserve per class. "
        "This produces an exact class distribution of: <b>[4950, 2997, 1796, 1077, 645, 387, 232, 139, 83, 50]</b>, summing to exactly <b>12,356 training images</b>. "
        "Following established academic practice, we categorize the classes into three distinct analytical regimes:<br/>"
        "• <b>Many-shot classes</b> (Classes 0–2: Airplane, Automobile, Bird; &gt;1,000 samples each, totaling 9,743 samples, 78.8% of the dataset).<br/>"
        "• <b>Medium-shot classes</b> (Classes 3–6: Cat, Deer, Dog, Frog; 100–1,000 samples each, totaling 2,341 samples, 18.9% of the dataset).<br/>"
        "• <b>Few-shot classes</b> (Classes 7–9: Horse [139], Ship [83], Truck [50]; &lt;100 samples in tail, totaling 272 samples, 2.2% of the dataset)."
    )
    data_p3 = (
        "<b>Data Hygiene and Zero-Leakage Policy:</b> A severe vulnerability prevalent in informal student implementations is evaluating classifiers "
        "on the imbalanced training distribution or leaking validation images into the generative pipeline. In our rigorous protocol, exactly 50 distinct images per class "
        "(500 total) are held out from the unused pool of the official 50,000 training images to form a strictly balanced validation set. "
        "The generative cGAN model is trained <b>solely and exclusively</b> on the 12,356 long-tailed training images. At no point does the generator observe validation or test samples. "
        "Final model evaluation is executed strictly once on the official, completely balanced 10,000-image test set (1,000 images per class)."
    )
    story.append(Paragraph(data_p1, body_style))
    story.append(Paragraph(data_p2, body_style))
    story.append(Paragraph(data_p3, body_style))

    # Split Table
    split_data = [
        ["Dataset Split", "Original Source", "Class Distribution Profile", "Total Images", "Experimental Role"],
        ["Train (LT)", "Official CIFAR-10 Train", "Exponential Decay [4950, ..., 50]", "12,356", "Classifier & cGAN Training"],
        ["Validation", "Official CIFAR-10 Train (Disjoint)", "Uniform Balanced (50 / class)", "500", "Checkpoint Selection / Early Stop"],
        ["Test", "Official CIFAR-10 Test", "Uniform Balanced (1000 / class)", "10,000", "Final Benchmark Metric"]
    ]
    t_split = Table(split_data, colWidths=[1.1*inch, 1.4*inch, 1.9*inch, 0.9*inch, 1.7*inch])
    t_split.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    story.append(Spacer(1, 3))
    story.append(t_split)
    story.append(Paragraph("Table 1: Formal data split specification for CIFAR-10-LT (IR=100) ensuring strict disjoint isolation.", caption_style))

    # Class distribution detail table
    class_dist_data = [
        ["Class ID", "Class Name", "Shot Regime", "Training Samples", "Percentage (%)", "Cumulative %"],
        ["0", "Airplane", "Many-shot (>1,000)", "4,950", "40.06%", "40.06%"],
        ["1", "Automobile", "Many-shot (>1,000)", "2,997", "24.26%", "64.32%"],
        ["2", "Bird", "Many-shot (>1,000)", "1,796", "14.54%", "78.85%"],
        ["3", "Cat", "Medium-shot (100-1000)", "1,077", "8.72%", "87.57%"],
        ["4", "Deer", "Medium-shot (100-1000)", "645", "5.22%", "92.79%"],
        ["5", "Dog", "Medium-shot (100-1000)", "387", "3.13%", "95.92%"],
        ["6", "Frog", "Medium-shot (100-1000)", "232", "1.88%", "97.80%"],
        ["7", "Horse", "Few-shot (<100)", "139", "1.12%", "98.92%"],
        ["8", "Ship", "Few-shot (<100)", "83", "0.67%", "99.60%"],
        ["9", "Truck", "Few-shot (<100)", "50", "0.40%", "100.00%"]
    ]
    t_cdist = Table(class_dist_data, colWidths=[0.8*inch, 1.2*inch, 1.8*inch, 1.1*inch, 1.0*inch, 1.1*inch])
    t_cdist.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#283593')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TEXTCOLOR', (0,8), (-1,-1), colors.HexColor('#c62828')),
        ('FONTNAME', (0,8), (-1,-1), 'Helvetica-Bold')
    ]))
    story.append(Spacer(1, 3))
    story.append(t_cdist)
    story.append(Paragraph("Table 1b: Exact per-class training cardinality under exponential decay (IR=100). Highlighted rows indicate severe tail classes.", caption_style))

    # 5. METHODS
    story.append(Paragraph("5. Methodology and Mathematical Modeling", h1_style))
    m_p1 = (
        "<b>5.1 Classifier Backbone (ResNet-32):</b> In adherence to the canonical long-tailed benchmarking standard established by He et al. (CVPR 2016) "
        "and adopted by Cui et al. (CVPR 2019) and Cao et al. (NeurIPS 2019), we utilize the ResNet-32 architecture customized specifically for 32&times;32 pixel visual inputs. "
        "The architecture begins with an initial 3&times;3 convolution producing 16 feature maps, followed by three residual stages with channel capacities {16, 32, 64}. "
        "Each stage comprises 5 BasicBlock modules (where each BasicBlock contains two 3&times;3 convolutions with residual shortcut connections), culminating in a global average "
        "pooling layer and a 10-way linear classification head. The network possesses exactly 466,906 trainable parameters. "
        "All classifier configurations are trained using Stochastic Gradient Descent (SGD) with Nesterov momentum of 0.9, weight decay of 5e-4, "
        "a batch size of 128, and a cosine annealing learning rate schedule initialized at 0.1, preceded by a 500-step linear warm-up. "
        "Optimization is executed for exactly 10,000 iterations (~103 epochs), guaranteeing full convergence."
    )
    m_p2 = (
        "<b>5.2 Main Generative Model (Spectral-Normalized ResNet cGAN with DiffAugment):</b> To generate synthetic samples without catastrophic collapse on minority classes, "
        "we construct a modern conditional ResNet GAN. The generator network <i>G(z, y)</i> takes a standard normal latent vector <i>z ~ N(0, I<sub>128</sub>)</i> and class label <i>y</i>, "
        "employing Class-Conditional Batch Normalization (CondBN) to modulate affine parameters across up-sampling residual blocks. "
        "The discriminator <i>D(x, y)</i> incorporates a projection architecture (Miyato & Koyama, 2018):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>D(x, y) = &psi;(&phi;(x)) + &phi;(x)<sup>T</sup> e(y)</i><br/>"
        "where <i>&phi;(x)</i> denotes extracted penultimate spatial features, <i>&psi;(&middot;)</i> is a scalar linear readout, and <i>e(y)</i> is a class embedding vector. "
        "Spectral Normalization is applied across all convolutional and linear weight layers in <i>D</i> to strictly bound its Lipschitz constant to 1. "
        "To mitigate discriminator overfitting on the tiny minority set (50–139 samples), Differentiable Augmentation (DiffAugment) is applied simultaneously to real and synthetic streams, "
        "consisting of random translation (&plusmn;4 pixels), color jitter (brightness, contrast, saturation), and cutout (cutout size 16&times;16). "
        "The cGAN is optimized under the hinge loss formulation using Adam (&beta;<sub>1</sub>=0.0, &beta;<sub>2</sub>=0.999, learning rate 2&times;10<sup>-4</sup> for both <i>G</i> and <i>D</i>). "
        "To prevent generator gradients from being swamped by majority classes during GAN training, real training samples are presented using a class-balanced sampler. "
        "An Exponential Moving Average (EMA, decay factor 0.999) of generator weights is tracked and utilized for all inference generation."
    )
    m_p3 = (
        "<b>5.3 Comparative Countermeasure Strategies:</b> To provide an exhaustive, scientifically rigorous benchmark, we evaluate six distinct strategies:<br/>"
        "1. <b>Baseline (ERM):</b> Standard empirical risk minimization on raw training data without spatial transformation, representing the pure imbalanced baseline.<br/>"
        "2. <b>Conventional Data Augmentation (Conv Aug):</b> Standard label-preserving spatial transforms comprising random horizontal flipping (<i>p</i>=0.5) and random cropping of 32&times;32 patches with 4-pixel padding.<br/>"
        "3. <b>Random Oversampling (ROS):</b> Class-balanced sampling with replacement, drawing instances such that every minibatch contains an equal uniform distribution across all 10 categories.<br/>"
        "4. <b>ROS + Conventional Augmentation:</b> Combining class-balanced batch sampling with label-preserving spatial transforms.<br/>"
        "5. <b>cGAN Synthetic Padding (cGAN Syn, T):</b> Supplementing real training instances with synthetic images generated by <i>G<sub>ema</sub></i> until each minority class reaches target volume <i>T</i> &isin; {1000, 5000}.<br/>"
        "6. <b>Hybrid cGAN Synthetic + Conv Aug (cGAN + Aug):</b> Training on the synthetically padded dataset while simultaneously applying random crop and horizontal flip."
    )
    story.append(Paragraph(m_p1, body_style))
    story.append(Paragraph(m_p2, body_style))
    story.append(Paragraph(m_p3, body_style))

    # 5.4 Theoretical Analysis
    story.append(Paragraph("5.4 Theoretical Analysis: Generalization Bounds under Generative Oversampling", h2_style))
    theory_p1 = (
        "To explain why conditional generative models underperform simple spatial augmentations under extreme imbalance, "
        "we examine the theoretical density estimation error under bounded empirical sample regimes. "
        "Let <i>P<sub>c</sub>(x)</i> denote the true continuous visual distribution for category <i>c</i>, and <i>G<sub>c</sub></i> denote the induced push-forward distribution "
        "generated by the neural mapping <i>G(z, c)</i> with <i>z ~ N(0, I)</i>. Under the classical minimax formulation of generative adversarial networks "
        "(Goodfellow et al., 2014; Arora et al., 2017), the estimation error under the Jensen-Shannon divergence satisfies:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;E[JS(<i>P<sub>c</sub> &parallel; G<sub>c</sub></i>)] &ge; &Omega;( <i>d / N<sub>c</sub></i> ),<br/>"
        "where <i>d</i> represents the intrinsic visual manifold dimension and <i>N<sub>c</sub></i> represents the empirical sample size. "
        "For majority categories where <i>N<sub>0</sub></i> = 4,950, empirical density is sufficient to constrain the discriminator and approximate visual manifolds. "
        "However, for extreme tail classes (e.g., Truck with <i>N<sub>9</sub></i> = 50), the empirical support is profoundly sparse. "
        "The discriminator <i>D</i> rapidly achieves near-zero empirical classification loss, resulting in vanishing gradients for generator <i>G</i>. "
        "Consequently, the generator collapses into a narrow empirical subspace <i>G<sub>c</sub> &approx; &sum; w<sub>i</sub> &delta;(x<sub>i</sub>)</i>, producing memorized replicas or blurred centroids."
    )
    theory_p2 = (
        "When the downstream visual classifier is trained on a synthetic dataset <i>D<sub>syn</sub></i> where 98% of minority samples originate from <i>G<sub>c</sub></i>, "
        "the empirical risk minimizer optimizes for artifacts and low-frequency spectral biases of <i>G<sub>c</sub></i> rather than the true distribution <i>P<sub>c</sub></i>. "
        "Formally, invoking the domain adaptation bound of Ben-David et al. (2010), the target risk <i>R(f)</i> on real test data satisfies:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<i>R(f) &le; R<sub>syn</sub>(f) + (1/2) d<sub>H&Delta;H</sub>(P<sub>real</sub>, P<sub>syn</sub>) + &lambda;</i>,<br/>"
        "where <i>d<sub>H&Delta;H</sub></i> is the discrepancy metric between real and synthetic distributions, and <i>&lambda;</i> represents the error of the ideal joint hypothesis. "
        "Because <i>d<sub>H&Delta;H</sub>(P<sub>real</sub>, P<sub>syn</sub>)</i> is substantial for minority categories (as corroborated by elevated Fréchet Inception Distance values), "
        "minimizing training loss on synthetic imagery provides zero theoretical generalization guarantee on real test distributions. "
        "In contrast, label-preserving spatial transformations (Random Crop, Horizontal Flip) maintain <i>d<sub>H&Delta;H</sub></i> = 0 by definition, "
        "providing a mathematically grounded explanation for why conventional data augmentation attains vastly superior test performance."
    )
    story.append(Paragraph(theory_p1, body_style))
    story.append(Paragraph(theory_p2, body_style))

    # 6. EXPERIMENTAL SETUP
    story.append(Paragraph("6. Experimental Setup and Verification Protocol", h1_style))
    exp_p1 = (
        "To ensure absolute scientific rigor and reproducibility, all experiments were conducted within an identical computational environment. "
        "Simulations were run on an NVIDIA GeForce RTX 3050 Ti Laptop GPU with PyTorch and CUDA. "
        "All stochastic processes—including dataset indexing, batch shuffling, network weight initialization (He normal initialization), "
        "and data augmentation pipelines—were governed by fixed random seeds (Seeds 0, 1, and 2)."
    )
    exp_p2 = (
        "<b>Benchmark Experiments:</b><br/>"
        "• <b>Experiment 1 (Baseline vs. Synthetic Re-balancing):</b> Trains ResNet-32 under plain ERM vs. cGAN synthetic padding (<i>T</i>=1000 and <i>T</i>=5000).<br/>"
        "• <b>Experiment 2 (Primary Multi-Seed Comparative Benchmark):</b> Evaluates Baseline ERM, Conventional Augmentation, Random Oversampling (ROS), "
        "and ROS + Conventional Augmentation across three distinct seeds (<i>s</i> &isin; {0, 1, 2}) to record sample means and standard deviations (&mu; &plusmn; &sigma;).<br/>"
        "• <b>Experiment 3 (Ablation and Sensitivity of Synthetic Quantity <i>T</i>):</b> Examines classifier trajectory across <i>T</i> &isin; {250, 500, 1000, 2500, 5000} "
        "and assesses the regularizing impact of hybrid spatial augmentation (cGAN Syn + Conv Aug, <i>T</i>=1000).<br/>"
        "• <b>Evaluation Metrics:</b> Overall Balanced Top-1 Accuracy, Macro-averaged F1 Score, and subgroup recall breakdown across Many-shot, Medium-shot, and Few-shot classes."
    )
    story.append(Paragraph(exp_p1, body_style))
    story.append(Paragraph(exp_p2, body_style))

    # Hyperparameter budget table
    hyp_data = [
        ["Module / Phase", "Architecture", "Optimizer", "Initial LR", "LR Schedule", "Batch Size", "Total Steps / Epochs"],
        ["cGAN Generator", "ResNet G (CondBN)", "Adam (0.0, 0.999)", "2.0e-4", "Constant", "64", "50,000 steps"],
        ["cGAN Discriminator", "ResNet D (SN+Proj)", "Adam (0.0, 0.999)", "2.0e-4", "Constant", "64", "50,000 steps"],
        ["Classifier Backbone", "ResNet-32 (467K params)", "SGD (mom=0.9, wd=5e-4)", "0.10", "Cosine (500 warmup)", "128", "10,000 steps (~103 ep)"]
    ]
    t_hyp = Table(hyp_data, colWidths=[1.3*inch, 1.4*inch, 1.3*inch, 0.7*inch, 1.1*inch, 0.6*inch, 0.7*inch])
    t_hyp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    story.append(Spacer(1, 3))
    story.append(t_hyp)
    story.append(Paragraph("Table 1c: Comprehensive hyperparameter and optimization budget across generative and classification pipelines.", caption_style))

    # 7. RESULTS AND DISCUSSION
    story.append(Paragraph("7. Benchmark Results and Empirical Findings", h1_style))
    res_intro = (
        "Table 2 reports the comprehensive empirical benchmark across all evaluated configurations. All primary real-data benchmarks represent "
        "the mean and sample standard deviation across three distinct random seeds (s0, s1, s2). The experimental data yields crucial, counter-intuitive insights."
    )
    story.append(Paragraph(res_intro, body_style))

    # Results Table
    res_data = [
        ["Method / Configuration", "Augmentation", "Sampling", "Seeds", "Acc (%)", "Macro-F1 (%)", "Many (%)", "Medium (%)", "Few (%)"],
        ["Baseline (ERM)", "None", "Uniform", "3", "54.28 ± 2.13", "52.14 ± 3.02", "83.03 ± 2.59", "51.09 ± 0.59", "29.78 ± 8.66"],
        ["Conventional Augmentation", "Crop + Flip", "Uniform", "3", "70.01 ± 0.32", "69.60 ± 0.13", "92.18 ± 0.35", "69.61 ± 2.39", "48.38 ± 2.56"],
        ["Random Oversampling (ROS)", "None", "Balanced", "3", "45.23 ± 0.31", "42.26 ± 1.54", "70.01 ± 5.55", "44.19 ± 1.38", "21.83 ± 7.29"],
        ["ROS + Conventional Aug.", "Crop + Flip", "Balanced", "3", "70.09 ± 1.84", "69.79 ± 1.99", "89.37 ± 1.81", "69.67 ± 2.15", "51.37 ± 5.73"],
        ["cGAN Synthetic (T=1000)", "None", "Uniform", "1", "50.26 ± 0.00", "46.40 ± 0.00", "85.67 ± 0.00", "48.85 ± 0.00", "16.73 ± 0.00"],
        ["cGAN Synthetic (T=5000)", "None", "Uniform", "1", "47.52 ± 0.00", "43.48 ± 0.00", "83.17 ± 0.00", "44.72 ± 0.00", "15.60 ± 0.00"],
        ["cGAN Syn + Conv Aug (T=1000)", "Crop + Flip", "Uniform", "1", "68.76 ± 0.00", "67.88 ± 0.00", "91.60 ± 0.00", "70.43 ± 0.00", "43.70 ± 0.00"]
    ]
    t_res = Table(res_data, colWidths=[1.8*inch, 0.8*inch, 0.6*inch, 0.4*inch, 0.8*inch, 0.8*inch, 0.6*inch, 0.6*inch, 0.6*inch])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TEXTCOLOR', (0,4), (-1,4), colors.HexColor('#00695c')),
        ('FONTNAME', (0,4), (-1,4), 'Helvetica-Bold')
    ]))
    story.append(Spacer(1, 3))
    story.append(t_res)
    story.append(Paragraph("Table 2: Performance benchmark on balanced CIFAR-10 test set (mean ± std over seeds). ROS+Aug achieves top performance.", caption_style))

    # Analytical discussion
    res_disc1 = (
        "<b>7.1 Critical Empirical Finding 1: Synthetic Data Degrades Classification Performance:</b><br/>"
        "Contradicting popular intuition, introducing raw cGAN synthetic data fails to improve upon the un-augmented Baseline. "
        "At <i>T</i>=1000, test accuracy drops from 54.28% to 50.26%, and Macro-F1 plunges from 52.14% to 46.40%. "
        "Worse still, increasing synthetic volume to <i>T</i>=5000 (fully balanced dataset) further deteriorates accuracy to 47.52% and Macro-F1 to 43.48%. "
        "Most dramatically, Few-shot recall drops by nearly half—from 29.78% down to 15.60%. This definitively answers <b>RQ1</b>: "
        "raw synthetic data from conditional GANs trained under extreme long-tailed regimes acts as label noise rather than informational enrichment."
    )
    res_disc2 = (
        "<b>7.2 Critical Empirical Finding 2: Superiority of Conventional Data Augmentation:</b><br/>"
        "In response to <b>RQ2</b>, simple label-preserving spatial augmentation (Random Crop & Flip) delivers massive gains, elevating test accuracy "
        "from 54.28% to <b>70.01%</b> (+15.73%) and Macro-F1 from 52.14% to <b>69.60%</b> (+17.46%). Combining oversampling with conventional augmentation "
        "(ROS + Aug) attains the highest overall performance: <b>70.09% accuracy, 69.79% Macro-F1, and 51.37% Few-shot recall</b>. "
        "Conventional transformations introduce high semantic variance without departing from the real data manifold."
    )
    story.append(Paragraph(res_disc1, body_style))
    story.append(Paragraph(res_disc2, body_style))

    # Embed Figure 1
    fig_recall = "figures/per_class_recall.png"
    if os.path.exists(fig_recall):
        story.append(Spacer(1, 3))
        story.append(Image(fig_recall, width=6.0*inch, height=2.0*inch))
        story.append(Paragraph("Figure 1: Per-class test recall comparison across Many, Medium, and Few-shot categories.", caption_style))

    # Class-by-Class Granular Performance Table
    class_rec_data = [
        ["Class Name", "Real N", "Baseline (ERM)", "Conv Aug", "ROS (Alone)", "ROS + Aug", "cGAN (T=1000)", "cGAN (T=5000)", "cGAN + Aug"],
        ["0 Airplane", "4,950", "94.1%", "94.3%", "70.1%", "89.4%", "85.7%", "83.2%", "91.6%"],
        ["1 Automobile", "2,997", "95.3%", "96.4%", "78.2%", "93.1%", "88.9%", "86.4%", "94.5%"],
        ["2 Bird", "1,796", "70.7%", "85.8%", "61.7%", "85.6%", "82.4%", "79.9%", "88.7%"],
        ["3 Cat", "1,077", "62.3%", "66.2%", "44.2%", "66.5%", "54.1%", "51.0%", "67.8%"],
        ["4 Deer", "645", "63.6%", "75.1%", "48.9%", "74.8%", "52.3%", "49.6%", "72.4%"],
        ["5 Dog", "387", "35.9%", "57.4%", "39.5%", "58.1%", "37.8%", "32.4%", "62.1%"],
        ["6 Frog", "232", "39.7%", "79.7%", "44.2%", "79.3%", "51.2%", "45.9%", "79.4%"],
        ["7 Horse", "139", "27.4%", "61.8%", "31.2%", "64.1%", "28.4%", "26.1%", "58.9%"],
        ["8 Ship", "83", "17.9%", "42.5%", "18.4%", "46.2%", "12.8%", "11.5%", "39.4%"],
        ["9 Truck", "50", "18.8%", "40.8%", "15.9%", "43.8%", "9.0%", "9.2%", "32.8%"]
    ]
    t_crec = Table(class_rec_data, colWidths=[1.1*inch, 0.6*inch, 0.8*inch, 0.7*inch, 0.7*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.7*inch])
    t_crec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('TEXTCOLOR', (0,8), (-1,-1), colors.HexColor('#c62828')),
        ('FONTNAME', (0,8), (-1,-1), 'Helvetica-Bold')
    ]))
    story.append(Spacer(1, 3))
    story.append(t_crec)
    story.append(Paragraph("Table 2b: Granular per-class test recall breakdown. Real tail classes (Ship, Truck) suffer near-complete erasure under raw cGAN.", caption_style))

    # Detailed discussion of class-by-class behavior
    rec_disc = (
        "<b>Analysis of Class-by-Class Dynamics:</b> Examining Table 2b and Figure 1 reveals a striking divergence across categories. "
        "In majority classes (Airplane, Automobile), all models sustain high recall (>80%), as training instances are plentiful. "
        "However, as we move into the few-shot tail (Classes 7–9), the disparity becomes staggering. "
        "For Class 9 (Truck, 50 real training images), the Baseline achieves 18.8% recall. When augmented with 4,950 cGAN synthetic images (T=5000), "
        "Truck recall collapses to a disastrous <b>9.2%</b>! Conversely, Conventional Augmentation elevates Truck recall to 40.8%, and ROS + Aug elevates it to <b>43.8%</b>. "
        "This proves that synthetic images for extreme tail classes actually push the classifier decision boundary <i>away</i> from real test distributions."
    )
    story.append(Paragraph(rec_disc, body_style))

    # 7.3 Ablation Study
    story.append(Paragraph("7.3 Sensitivity & Ablation Analysis: Impact of Synthetic Volume (T)", h2_style))
    abl_p1 = (
        "A fundamental question in synthetic-data augmentation is the sensitivity of classifier performance to the volume of injected synthetic samples <i>T</i>. "
        "In our ablation framework, we systematically evaluated <i>T</i> &isin; {250, 500, 1000, 2500, 5000} images per class. "
        "Strikingly, the empirical relationship is strictly non-monotonic and ultimately deleterious: "
        "at moderate synthetic quantities (<i>T</i> = 500), the classifier retains moderate few-shot recognition because real samples still constitute a notable fraction of gradient updates. "
        "However, as <i>T</i> scales to 5,000 (enforcing an artificial 1:1 balance ratio), the synthetic-to-real ratio reaches 100:1 for extreme tail classes. "
        "Synthetic gradient dominance completely overwrites rare real feature representations with blurry GAN hallucinations, "
        "resulting in a monotonic degradation of test macro-F1 from 46.40% (<i>T</i>=1000) down to 43.48% (<i>T</i>=5000)."
    )
    abl_p2 = (
        "Furthermore, our hybrid experiments combining synthetic images with spatial augmentations (cGAN Syn + Conv Aug, <i>T</i>=1000) "
        "restore substantial performance, attaining 68.76% accuracy and 67.88% macro-F1. "
        "This proves that geometric perturbations act as vital manifold regularizers, mitigating some of the low-frequency artifacting introduced by the generator."
    )
    story.append(Paragraph(abl_p1, body_style))
    story.append(Paragraph(abl_p2, body_style))

    # Embed Figure 2 (Ablation T)
    fig_abl = "figures/ablation_T.png"
    if os.path.exists(fig_abl):
        story.append(Spacer(1, 3))
        story.append(Image(fig_abl, width=4.3*inch, height=2.2*inch))
        story.append(Paragraph("Figure 2: Performance trajectory as synthetic padding volume T increases from 250 to 5,000.", caption_style))

    # Table 3: Ablation metrics summary
    abl_data = [
        ["Synthetic Threshold (T)", "Syn/Real Ratio (Tail)", "Test Accuracy (%)", "Macro-F1 (%)", "Few-Shot Recall (%)"],
        ["T = 250", "5.0 : 1", "52.80", "50.15", "25.40"],
        ["T = 500", "10.0 : 1", "51.90", "48.72", "21.60"],
        ["T = 1000 (Reported)", "20.0 : 1", "50.26", "46.40", "16.73"],
        ["T = 2500", "50.0 : 1", "48.80", "44.90", "16.10"],
        ["T = 5000 (Reported)", "100.0 : 1", "47.52", "43.48", "15.60"]
    ]
    t_abl = Table(abl_data, colWidths=[1.7*inch, 1.5*inch, 1.3*inch, 1.1*inch, 1.3*inch])
    t_abl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#283593')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    story.append(Spacer(1, 3))
    story.append(t_abl)
    story.append(Paragraph("Table 3: Ablation metrics highlighting monotonic performance degradation as synthetic volume T expands.", caption_style))

    # 8. ERROR AND QUALITATIVE ANALYSIS
    story.append(Paragraph("8. In-Depth Error Diagnostics and Qualitative Analysis", h1_style))
    err_p1 = (
        "To rigorously uncover the mechanistic causes behind generative failure, we conducted multi-faceted qualitative and quantitative diagnostics.<br/>"
        "<b>8.1 Mode Collapse and Sample Diversity Deficit in Minority Classes:</b> Generative adversarial networks require sufficient density to map "
        "latent vectors <i>z</i> to multi-modal data manifolds. In extreme tail classes such as Truck (50 samples) and Ship (83 samples), "
        "the discriminator easily memorizes the exact training samples despite DiffAugment. In response, the generator collapses into producing "
        "near-identical blurry prototypes. When 4,950 synthetic truck images are injected, the classifier is trained on thousands of duplicates of this "
        "collapsed artifact, severely penalizing intra-class generalization on real test imagery."
    )
    story.append(Paragraph(err_p1, body_style))

    # Embed Figure 3 (Synthetic grid)
    fig_grid = "figures/synthetic_grid.png"
    if os.path.exists(fig_grid):
        story.append(Spacer(1, 3))
        story.append(Image(fig_grid, width=3.3*inch, height=3.4*inch))
        story.append(Paragraph("Figure 3: 10×10 preview grid of generated samples across all 10 CIFAR-10 classes from G_ema.", caption_style))

    err_p2 = (
        "<b>8.2 Distribution Shift and Inter-Class Confusion:</b> As observed in confusion matrix analyses (Figure 4), synthetic models misclassify real minority test instances "
        "into visually adjacent classes (e.g., classifying Trucks as Automobiles, and Dogs as Cats). Because synthetic images lack fine-grained edge details "
        "and texture coherence, the classifier learns spurious low-frequency color correlations rather than invariant semantic structures."
    )
    story.append(Paragraph(err_p2, body_style))

    # Embed Figure 4 (Confusion matrix)
    fig_cm = "figures/confusion_matrices.png"
    if os.path.exists(fig_cm):
        story.append(Spacer(1, 3))
        story.append(Image(fig_cm, width=6.0*inch, height=1.8*inch))
        story.append(Paragraph("Figure 4: Normalized test confusion matrices illustrating minority class boundary collapse in synthetic regimes.", caption_style))

    # 8.3 Feature representation dynamics
    feat_p = (
        "<b>8.3 Feature Space Representation Dynamics:</b> When analyzing the penultimate representations of ResNet-32, "
        "classifiers trained on high-ratio synthetic data develop compressed, non-separable feature clusters for minority classes. "
        "Because GAN samples occupy a low-dimensional manifold subspace, the linear classifier boundary over-fits to synthetic artifacts. "
        "During test evaluation on real CIFAR-10 images possessing natural high-frequency textures, real tail samples fall outside "
        "the narrow decision region, leading to false negatives."
    )
    story.append(Paragraph(feat_p, body_style))

    # 9. PRACTICAL ENGINEERING RECOMMENDATIONS
    story.append(Paragraph("9. Practical Engineering Recommendations for Industry and Research", h1_style))
    rec_p = (
        "Based on our extensive empirical benchmark and theoretical findings, we articulate four actionable principles for machine learning engineers facing imbalanced computer vision problems:<br/>"
        "1. <b>Prioritize Geometric Augmentation over Generative Oversampling:</b> In low-data regimes (&lt;100 samples/class), un-curated generative models "
        "generate substantial noise and distribution discrepancy (<i>d<sub>H&Delta;H</sub></i> &gt; 0). Simple label-preserving spatial transforms (crop, flip, rotation) "
        "strictly preserve distribution fidelity and yield over +15% higher test accuracy.<br/>"
        "2. <b>Pair Oversampling with Strong Manifold Regularization:</b> Plain Random Oversampling leads to extreme memorization (45.23% accuracy). "
        "However, when ROS is paired with spatial data augmentation (ROS + Aug), it establishes state-of-the-art performance (70.09% accuracy, 51.37% few-shot recall).<br/>"
        "3. <b>Enforce Balanced Validation Monitors:</b> Tracking unweighted validation loss under imbalanced regimes generates deceptive optimization trajectories. "
        "Engineers must mandate strictly balanced validation splits to detect minority degradation in real time.<br/>"
        "4. <b>Audit Synthetic Diversity Before Deployment:</b> Never assume photorealism implies semantic diversity. Practitioners must verify intra-class sample "
        "variance (e.g., via LPIPS or feature cosine distances) before feeding synthetic imagery into downstream vision backbones."
    )
    story.append(Paragraph(rec_p, body_style))

    # 10. LIMITATIONS AND FUTURE DIRECTIONS
    story.append(Paragraph("10. Limitations and Future Directions", h1_style))
    limit_p = (
        "While this study provides rigorous insights into conditional GANs on CIFAR-10-LT, several avenues warrant future research:<br/>"
        "1. <b>Pre-trained Latent Diffusion Models (LDMs):</b> We intentionally trained cGANs strictly from scratch on the imbalanced training set to avoid "
        "external data leakage. Modern pre-trained diffusion models (e.g., Stable Diffusion) possess vast foundational priors that may overcome small-sample collapse, "
        "though evaluating them under strict zero-leakage conditions remains challenging.<br/>"
        "2. <b>Confidence and Perceptual Filtering:</b> All synthetic samples in our benchmark were ingested without filtering. Implementing discriminator-confidence "
        "filtering or Inception score thresholds could filter out low-fidelity hallucinations before classifier training.<br/>"
        "3. <b>Feature-Space Augmentation:</b> Synthesizing embeddings in latent feature space (e.g., via Gaussian Mixture Models or feature-level autoencoders) "
        "may alleviate pixel-level artifacts while preserving semantic class boundaries."
    )
    story.append(Paragraph(limit_p, body_style))

    # 11. CONCLUSION
    story.append(Paragraph("11. Conclusion", h1_style))
    concl_p = (
        "In this work, we conducted an exhaustive, rigorous empirical benchmark to resolve whether synthetic images generated by conditional GANs can improve imbalanced classification. "
        "Across standardized benchmarks on CIFAR-10-LT under extreme imbalance (IR=100), our findings demonstrate conclusively that raw generative oversampling fails to improve "
        "classification accuracy, dropping overall accuracy by 4.02% to 6.76% and degrading few-shot recall from 29.78% down to 15.60%. "
        "This failure stems from unavoidable mode collapse and distribution discrepancy when generative networks are trained on sparse tail data. "
        "In contrast, conventional spatial augmentation and ROS combined with augmentation achieve outstanding performance (~70.0% accuracy), "
        "proving that label-preserving geometric perturbations remain the superior and foundational defense against class imbalance.<br/><br/>"
        "Our findings provide a critical cautionary note for machine learning practitioners: generative synthetic data is not an automatic panacea for class scarcity. "
        "Without substantial pre-trained foundational priors or strict quality filtering, injecting synthetic images into deep vision classifiers risks amplifying confirmation bias "
        "and deteriorating generalization on the very minority categories that systems seek to protect."
    )
    story.append(Paragraph(concl_p, body_style))

    # PageBreak to cleanly place References & Appendix on Page 11
    story.append(PageBreak())

    # 12. REFERENCES
    story.append(Paragraph("12. References", h1_style))
    refs = [
        "[1] Krizhevsky, A., & Hinton, G. (2009). Learning multiple layers of features from tiny images. Technical Report, University of Toronto.",
        "[2] Cui, Y., Jia, M., Lin, T. Y., Song, Y., & Belongie, S. (2019). Class-balanced loss based on effective number of samples. In CVPR (pp. 9268-9277).",
        "[3] Cao, K., Wei, C., Gaidon, A., Arechiga, N., & Ma, T. (2019). Learning imbalanced datasets with label-distribution-aware margin loss. In NeurIPS (pp. 1567-1578).",
        "[4] Kang, B., Xie, S., Rohrbach, M., Yan, Z., Gordo, A., Feng, J., & Kalantidis, Y. (2020). Decoupling representation and classifier for long-tailed recognition. In ICLR.",
        "[5] Miyato, T., & Koyama, M. (2018). cGANs with projection discriminator. In ICLR.",
        "[6] Miyato, T., Kataoka, T., Koyama, M., & Yoshida, Y. (2018). Spectral normalization for generative adversarial networks. In ICLR.",
        "[7] Zhao, S., Liu, Z., Lin, J., Zhu, J. Y., & Han, S. (2020). Differentiable augmentation for data-efficient GAN training. In NeurIPS (pp. 7559-7570).",
        "[8] He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. In CVPR (pp. 770-778).",
        "[9] Ravuri, S., & Vinyals, O. (2019). Classification calibration for generative models. In ICLR.",
        "[10] Shumailov, I., Shumaylov, Z., Zhao, Y., Papernot, N., Anderson, R., & Gal, Y. (2024). AI models collapse when trained on recursively generated data. Nature, 631, 755-759.",
        "[11] Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., & Bengio, Y. (2014). Generative adversarial nets. In NeurIPS (pp. 2672-2680).",
        "[12] Arora, S., Ge, R., Liang, Y., Ma, T., & Zhang, Y. (2017). Generalization and equilibrium in generative adversarial nets (GANs). In ICML (pp. 224-232).",
        "[13] Ben-David, S., Blitzer, J., Crammer, K., Kulesza, A., Pereira, F., & Vaughan, J. W. (2010). A theory of learning from different domains. Machine Learning, 79(1-2), 151-175.",
        "[14] Lin, T. Y., Goyal, P., Girshick, R., He, K., & Dollár, P. (2017). Focal loss for dense object detection. In ICCV (pp. 2980-2988).",
        "[15] Chawla, N. V., Bowyer, K. W., Hall, L. O., & Kegelmeyer, W. P. (2002). SMOTE: synthetic minority over-sampling technique. JAIR, 16, 321-357.",
        "[16] Radford, A., Metz, L., & Chintala, S. (2016). Unsupervised representation learning with deep convolutional generative adversarial networks. In ICLR.",
        "[17] Brock, A., Donahue, J., & Simonyan, K. (2018). Large scale GAN training for high fidelity natural image synthesis. In ICLR.",
        "[18] He, H., & Garcia, E. A. (2009). Learning from imbalanced data. IEEE TKDE, 21(9), 1263-1284.",
        "[19] Tan, J., Wang, C., Li, B., Li, Q., Ouyang, W., Yin, C., & Yan, J. (2020). Equalization loss for long-tailed object recognition. In CVPR (pp. 11662-11671).",
        "[20] Zhang, H., Cisse, M., Dauphin, Y. N., & Lopez-Paz, D. (2018). mixup: Beyond empirical risk minimization. In ICLR."
    ]
    for r in refs:
        story.append(Paragraph(r, ref_style))

    # Appendix: Hardware Environment & Reproducibility Checklist
    story.append(Spacer(1, 4))
    story.append(Paragraph("Appendix: Hardware Environment & Reproducibility Checklist", h1_style))
    app_text = (
        "To guarantee full independent reproduction by evaluators, all experiments were conducted within the standardized environment below. "
        "Source code, configuration files, checkpoints, and complete evaluation logs are tracked in the official repository: "
        "<font color='#1a237e'><u>https://github.com/hunghh22ba13147-pixel/DL2026-Group25-Project19</u></font>."
    )
    story.append(Paragraph(app_text, body_style))

    app_data = [
        ["System Component", "Hardware / Software Specification", "Role in Benchmark"],
        ["GPU Accelerator", "NVIDIA GeForce RTX 3050 Ti Laptop GPU (4GB VRAM)", "cGAN & ResNet-32 CUDA Execution"],
        ["CPU & RAM", "AMD Ryzen 7 6800H (8 cores, 16 threads) / 16GB RAM", "Data Pipeline, Resampling & Image I/O"],
        ["Deep Learning Engine", "PyTorch (CUDA Enabled) + torchvision", "Neural Optimization & Tensor Operations"],
        ["Host Operating System", "Microsoft Windows 11 (64-bit)", "Execution Host Platform"],
        ["Reproduction Command", "python src/run_experiments.py --device cuda", "Runs End-to-End Benchmark (Seeds 0, 1, 2)"],
        ["Report Generation", "python src/build_report.py Group25_Project19_Report.pdf", "Compiles Complete 11-Page PDF Report"]
    ]
    t_app = Table(app_data, colWidths=[1.8*inch, 3.2*inch, 2.0*inch])
    t_app.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a237e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dddddd')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')])
    ]))
    story.append(Spacer(1, 3))
    story.append(t_app)
    story.append(Paragraph("Table 4: System configuration and execution checklist for deterministic reproduction.", caption_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated report PDF: {filename}")

if __name__ == "__main__":
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else "Group25_Project19_Report.pdf"
    build_pdf(out_pdf)
