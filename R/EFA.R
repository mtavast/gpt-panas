setwd("/u/96/tavastm1/unix/Desktop/iui2022/PANAS/")
### DAVINCI

library(patchwork)
library(psych)
library(nFactors)
library(ggplot2)
library(dplyr)
library(xtable)

# Place this script into the same folder with data csv file
folder <- "/u/96/tavastm1/unix/Desktop/iui2022/PANAS/"

filepath1 = paste(folder, "/Output/PANAS_bl_ada_R1.csv", sep="")
filepath2 = paste(folder, "/Output/PANAS_bl_babbage_R1.csv", sep="")
filepath3 = paste(folder, "/Output/PANAS_bl_curie_R1.csv", sep="")
filepath4 = paste(folder, "/Output/PANAS_bl_davinci_R1.csv", sep="")
filepath5 = paste(folder, "/HumanData/PANAS_SESOI.csv", sep="")


dat1 <- read.csv(filepath1)
dat2 <- read.csv(filepath2)
dat3 <- read.csv(filepath3)
dat4 <- read.csv(filepath4)
dat5 <- read.csv(filepath5)

# Make every data have the same variable order
dat1 <- dat1 %>% 
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud,
                attentive, scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)
dat2 <- dat2 %>% 
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud,
                attentive, scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)
dat3 <- dat3 %>% 
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud,
                attentive, scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)
dat4 <- dat4 %>% 
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud,
                attentive, scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)
dat5 <- dat5 %>% 
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud,
                attentive, scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)

var_names <- c("Enthusiastic", "Interested", "Determined", "Excited", "Inspired", 
               "Alert", "Active", "Strong", "Proud","Attentive", "Scared", "Afraid", 
               "Upset", "Distressed", "Jittery", "Nervous", "Ashamed", "Guilty", 
               "Irritable", "Hostile")



nsc1 <-nScree(dat1, model="factors")
nsc2 <-nScree(dat2, model="factors")
nsc3 <-nScree(dat3, model="factors")
nsc4 <-nScree(dat4, model="factors")
nsc5 <-nScree(dat5, model="factors")

plotnScree(nsc1, main='Ada')
plotnScree(nsc2, main='Babbage')
plotnScree(nsc3, main='Curie')
plotnScree(nsc4, main='Davinci')
plotnScree(nsc5, main='SESOI (human)')

screetab <- rbind(nsc1$Components,
      nsc2$Components,
      nsc3$Components,
      nsc4$Components,
      nsc5$Components)


g1 <- ggplot(nsc1$Analysis) +
  geom_line(aes(x = 1:20, y = Eigenvalues)) +
  geom_point(aes(x = 1:20, y = Eigenvalues), size=1) +
  geom_hline(yintercept = 1, lty=2, size=0.33) +
  xlab("Factors") + 
  ylab("Eigenvalues") +
  theme_bw() + 
  scale_y_continuous(limits = c(-1, 13), breaks = -1:13) +
  ggtitle("GPT-3 Ada") +
  theme(panel.grid = element_blank(),
        plot.title = element_text(size=18, hjust = 0.5),
        axis.title = element_text(size=15),
        axis.text.y = element_text(size=12))

g2 <- ggplot(nsc2$Analysis) +
  geom_line(aes(x = 1:20, y = Eigenvalues)) +
  geom_point(aes(x = 1:20, y = Eigenvalues), size=1) +
  geom_hline(yintercept = 1, lty=2, size=0.33) +
  xlab("Factors") + 
  ylab("Eigenvalues") +
  theme_bw() + 
  scale_y_continuous(limits = c(-1, 13), breaks = -1:13) +
  ggtitle("GPT-3 Babbage") +
  theme(panel.grid = element_blank(),
        axis.title.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(size=18, hjust = 0.5),
        axis.title = element_text(size=15))

g3 <- ggplot(nsc3$Analysis) +
  geom_line(aes(x = 1:20, y = Eigenvalues)) +
  geom_point(aes(x = 1:20, y = Eigenvalues), size=1) +
  geom_hline(yintercept = 1, lty=2, size=0.33) +
  xlab("Factors") + 
  ylab("Eigenvalues") +
  theme_bw() + 
  scale_y_continuous(limits = c(-1, 13), breaks = -1:13) +
  ggtitle("GPT-3 Curie") +
  theme(panel.grid = element_blank(),
        axis.title.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(size=18, hjust = 0.5),
        axis.title = element_text(size=15))

g4 <- ggplot(nsc4$Analysis) +
  geom_line(aes(x = 1:20, y = Eigenvalues)) +
  geom_point(aes(x = 1:20, y = Eigenvalues), size=1) +
  geom_hline(yintercept = 1, lty=2, size=0.33) +
  xlab("Factors") + 
  ylab("Eigenvalues") +
  theme_bw() + 
  scale_y_continuous(limits = c(-1, 13), breaks = -1:13) +
  ggtitle("GPT-3 Davinci") +
  theme(panel.grid = element_blank(),
        axis.title.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(size=18, hjust = 0.5),
        axis.title = element_text(size=15))

g5 <- ggplot(nsc5$Analysis) +
  geom_line(aes(x = 1:20, y = Eigenvalues)) +
  geom_point(aes(x = 1:20, y = Eigenvalues), size=1) +
  geom_hline(yintercept = 1, lty=2, size=0.33) +
  xlab("Factors") + 
  ylab("Eigenvalues") +
  theme_bw() + 
  scale_y_continuous(limits = c(-1, 13), breaks = -1:13) +
  ggtitle("Human Data [1]") +
  theme(panel.grid = element_blank(),
        axis.title.y = element_blank(),
        axis.ticks.y = element_blank(),
        axis.text.y = element_blank(),
        plot.title = element_text(size=18, hjust = 0.5),
        axis.title = element_text(size=15))

gfinal <- g1+g2+g3+g4 +
  plot_layout(ncol=4)

# Paper figure
gfinal2 <- g1+g2+g3+g4+g5 +
  plot_layout(nrow=1, ncol=5)

# Poster figure (with title)
gfinal2_poster <- g1+g2+g3+g4+g5 +
  plot_layout(nrow=1, ncol=5) +
  plot_annotation(title = "Scree plots", theme = theme(plot.title = element_text(size=22, hjust = 0.5, vjust = 2)))

ggsave("Figures/screeplots.png", gfinal, dpi = 300, width = 15, height = 4)
ggsave("Figures/screeplots_with_human.png", gfinal2, dpi = 300, width = 15, height = 4)
ggsave("Figures/screeplots_with_human_poster.png", gfinal2_poster, dpi = 300, width = 15, height = 4)


# Principal axis factor analysis, 2 factors, varimax rotation
fa1 <- psych::fa(dat1, 2, rotate="varimax", fm="pa")
fa2 <- psych::fa(dat2, 2, rotate="varimax", fm="pa")
fa3 <- psych::fa(dat3, 2, rotate="varimax", fm="pa")
fa4 <- psych::fa(dat4, 2, rotate="varimax", fm="pa")
fa5 <- psych::fa(dat5, 2, rotate="varimax", fm="pa")

# Factor correlations (not sure)
#round(fa1$score.cor, digits=2)
#round(fa2$score.cor, digits=2)
#round(fa3$score.cor, digits=2)
#round(fa4$score.cor, digits=2)
#round(fa5$score.cor, digits=2)

# LOADINGS
l1 <- matrix(round(fa1$loadings[1:40], 2), ncol=2, nrow=20)
l2 <- matrix(round(fa2$loadings[1:40], 2), ncol=2, nrow=20)
l3 <- matrix(round(fa3$loadings[1:40], 2), ncol=2, nrow=20)
l4 <- matrix(round(fa4$loadings[1:40], 2), ncol=2, nrow=20)
l5 <- matrix(round(fa5$loadings[1:40], 2), ncol=2, nrow=20)


mat <- cbind(l1, l2, l3, l4, l5) 

mat[abs(mat) < .25] = ""

dat <- as.data.frame(mat)
names(dat) <- rep(c("POS", "NEG"), 5)
rownames(dat) <- c(var_names)

# Print tex table
print(xtable(dat, type = "latex"), file = "fit.tex")

mat <- cbind(
round(c(fa3$TLI, fa4$TLI, fa5$TLI), 2),
round(c(fa3$RMSEA[1], fa4$RMSEA[1], fa5$RMSEA[1]), 2),
round(c(fa3$Vaccounted[3,2], fa4$Vaccounted[3,2], fa5$Vaccounted[3,2]), 2)
)

rownames(mat) <- c("GPT-3 Curie", "GPT-3 Davinci", "Anvari & Lakens (2021)")
colnames(mat) <- c("TLI", "RMSEA", "Var explained")

dat <- as.data.frame(mat)

# Print tex table
print(xtable(dat, type = "latex"), file = "fit_indices.tex")


round(fa3$RMSEA, digits=2)
round(fa4$RMSEA, digits=2)
round(fa5$RMSEA, digits=2)
round(fa3$TLI, digits=2)
round(fa4$TLI, digits=2)
round(fa5$TLI, digits=2)
round(fa3$Vaccounted, digits=2)
round(fa4$Vaccounted, digits=2)
round(fa5$Vaccounted, digits=2)


# Item correlations, correlation between sum of positive and sum of negative items
# Curie
dat3_pos <- dat3 %>%
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud, attentive)
dat3_neg <- dat3 %>%
  dplyr::select(scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)

pos_sum3 <- rowMeans(dat3_pos)
neg_sum3 <- rowMeans(dat3_neg)

print("CURIE:")
round(cor(pos_sum3, neg_sum3), digits=2)

# Davinci
dat4_pos <- dat4 %>%
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud, attentive)
dat4_neg <- dat4 %>%
  dplyr::select(scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)

pos_sum4 <- rowMeans(dat4_pos)
neg_sum4 <- rowMeans(dat4_neg)

print("DAVINCI:")
round(cor(pos_sum4, neg_sum4), digits=2)

# Human data
dat5_pos <- dat5 %>%
  dplyr::select(enthusiastic, interested, determined, excited, inspired, alert, active, strong, proud, attentive)
dat5_neg <- dat5 %>%
  dplyr::select(scared, afraid, upset, distressed, jittery, nervous, ashamed, guilty, irritable, hostile)

pos_sum5 <- rowMeans(dat5_pos)
neg_sum5 <- rowMeans(dat5_neg)
print("HUMAN:")
round(cor(pos_sum5, neg_sum5), digits=2)
