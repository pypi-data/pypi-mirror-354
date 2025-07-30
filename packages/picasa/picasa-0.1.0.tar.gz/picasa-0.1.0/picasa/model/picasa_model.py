import torch
torch.manual_seed(0)
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
import random 
import logging
logger = logging.getLogger(__name__)


		  
class Stacklayers(nn.Module):
	"""
	Stacklayers
  
	Parameters
	----------
	input_size: dimension of the input vector
	layers: list with hidden layer sizes
	dropout: proportion for dropout

	"""
	def __init__(self,input_size,layers,dropout=0.1):
		super(Stacklayers, self).__init__()
		self.layers = nn.ModuleList()
		self.input_size = input_size
		for next_l in layers:
			self.layers.append(nn.Linear(self.input_size,next_l))
			self.layers.append(nn.BatchNorm1d(next_l))
			self.layers.append(self.get_activation())
			self.layers.append(nn.Dropout(dropout))
			self.input_size = next_l

	def forward(self, input_data):
		for layer in self.layers:
			input_data = layer(input_data)
		return input_data

	def get_activation(self):
		return nn.ReLU()

class MLP(nn.Module):
	def __init__(self,
		input_dims:int,
		layers:list
		):
		super(MLP, self).__init__()
		
		self.fc = Stacklayers(input_dims,layers)

	def forward(self, x:torch.tensor):
		z = self.fc(x)
		return z

###### PICASA COMMON MODEL #######

class PICASACommonOut:
	def __init__(self,h_c1,h_c2,z_c1,z_c2,attn_c1, attn_c2):
		self.h_c1 = h_c1
		self.h_c2 = h_c2
		self.z_c1 = z_c1
		self.z_c2 = z_c2
		self.attn_c1 = attn_c1
		self.attn_c2 = attn_c2
				   
class GeneEmbedor(nn.Module):
	
	def __init__(self,
		emb_dim:int,
		out_dim:int,
		):
		super(GeneEmbedor, self).__init__()
		
		self.embedding = nn.Embedding(emb_dim,out_dim)
		self.emb_norm = nn.LayerNorm(out_dim)
		self.emb_dim = emb_dim

	def forward(self,
		x:torch.tensor):
		
		row_sums = x.sum(dim=1, keepdim=True)
		x_norm = torch.div(x, row_sums) * (self.emb_dim -1)
		return self.emb_norm(self.embedding(x_norm.int()))

class ScaledDotAttention(nn.Module):
	
	def __init__(self,
		weight_dim:int,
		pair_importance_weight:float=0.0
		):
		super(ScaledDotAttention, self).__init__()
		
		self.W_query = nn.Parameter(torch.randn(weight_dim, weight_dim))
		self.W_key = nn.Parameter(torch.randn(weight_dim, weight_dim))
		self.W_value = nn.Parameter(torch.randn(weight_dim, weight_dim))
		self.model_dim = weight_dim
		self.pair_importance_weight = pair_importance_weight
		
	def forward(self,
		query:torch.tensor, 
		key:torch.tensor, 
		value:torch.tensor
		):

		query_proj = torch.matmul(query, self.W_query)
		key_proj = torch.matmul(key, self.W_key)
		value_proj = torch.matmul(value, self.W_value)
		
		scores = torch.matmul(query_proj, key_proj.transpose(-2, -1)) / torch.sqrt(torch.tensor(self.model_dim).float())
					
		diag_bias = torch.eye(scores.shape[1], dtype=scores.dtype, device=scores.device) * torch.max(scores)
		p_importance = self.pair_importance_weight * diag_bias        
		scores = scores + p_importance
	
		attention_weights = torch.softmax(scores, dim=-1)
		output = torch.matmul(attention_weights, value_proj)

		return output, attention_weights

class AttentionPooling(nn.Module):

	def __init__(self, 
		model_dim:int
		):
		super(AttentionPooling, self).__init__()
		
		self.weights = nn.Parameter(torch.randn(model_dim))  
	
	def forward(self, 
		attention_output:torch.tensor
		):
		
		weights_softmax = torch.softmax(self.weights, dim=0)
		weighted_output = attention_output * weights_softmax.unsqueeze(0)
		pooled_output = torch.sum(weighted_output, dim=-1, keepdim=True)
		return pooled_output.squeeze(-1)

class ENCODER(nn.Module):
	def __init__(self,
		input_dims:int,
		layers:list
		):
		super(ENCODER, self).__init__()
		self.fc = Stacklayers(input_dims,layers)
  
	def forward(self, x:torch.tensor):
		return self.fc(x)

class ProjectorX(nn.Module):

	def __init__(self, 
		input_dim:int,
		output_dim:int
		):
		super(ProjectorX,self).__init__()
		
		self.output_transform = nn.Linear(input_dim, output_dim, bias=False)
		nn.init.orthogonal_(self.output_transform.weight)  
		
		for param in self.output_transform.parameters():
			param.requires_grad = False  
	
	def forward(self, 
		x:torch.tensor
		):
		
		output = self.output_transform(x)
		return output
	
	
class PICASACommonNet(nn.Module):
	def __init__(self,
		input_dim:int, 
		embedding_dim:int, 
		attention_dim:int, 
		latent_dim:int,
		encoder_layers:list,
		projection_layers:list,
		corruption_tol:float,
		pair_importance_weight:float
		):
		super(PICASACommonNet,self).__init__()

		self.embedding = GeneEmbedor(embedding_dim,attention_dim)
		
		self.attention = ScaledDotAttention(attention_dim,pair_importance_weight)
		
		self.pooling = AttentionPooling(attention_dim)

		self.encoder = ENCODER(input_dim,encoder_layers)
		
		self.projector_cl = MLP(latent_dim, projection_layers)
				
		self.corruption_tol = corruption_tol
		
		self.apply(self._init_weights)

	def _init_weights(self, module):
		if isinstance(module, nn.Linear):
			init.xavier_uniform_(module.weight)
			if module.bias is not None:
				init.zeros_(module.bias)
		elif isinstance(module, nn.Embedding):
			init.xavier_uniform_(module.weight)
		elif isinstance(module, nn.Parameter):
			init.xavier_uniform_(module)
			
	def forward(self,x_c1,x_c2,nbr_weight=None):
		
		if nbr_weight != None:
			mean_val = torch.mean(nbr_weight)
			std_val = torch.std(nbr_weight)
			threshold = self.corruption_tol * std_val
			outliers = torch.where(torch.abs(nbr_weight - mean_val) > threshold)
			outlier_indices = outliers[0]
			
			all_indices = torch.arange(nbr_weight.size(0))
			non_outlier_indices = torch.tensor([i for i in all_indices if i not in outlier_indices])
			sampled_indices = random.sample(non_outlier_indices.tolist(), len(outlier_indices))

			x_c1[outlier_indices] = x_c1[sampled_indices]
			x_c2[outlier_indices] = x_c2[sampled_indices]

		x_c1_emb = self.embedding(x_c1)
		x_c2_emb = self.embedding(x_c2)
  
		x_c1_att_out, x_c1_att_w = self.attention(x_c1_emb,x_c2_emb,x_c2_emb)
		x_c1_pool_out = self.pooling(x_c1_att_out)
		
		x_c2_att_out, x_c2_att_w = self.attention(x_c2_emb,x_c1_emb,x_c1_emb)
		x_c2_pool_out = self.pooling(x_c2_att_out)

		h_c1 = self.encoder(x_c1_pool_out)
		h_c2 = self.encoder(x_c2_pool_out)

		z_c1 = self.projector_cl(h_c1)
		z_c2 = self.projector_cl(h_c2)
		
		return PICASACommonOut(h_c1,h_c2,z_c1,z_c2,x_c1_att_w,x_c2_att_w)

	def estimate(self,x_c1):
     
		x_c1_emb = self.embedding(x_c1)
  
		x_c1_att_out, x_c1_att_w = self.attention(x_c1_emb,x_c1_emb,x_c1_emb)
		x_c1_pool_out = self.pooling(x_c1_att_out)
		
		h_c1 = self.encoder(x_c1_pool_out)

		z_c1 = self.projector_cl(h_c1)
		
		h_c2 = None
		z_c2 = None
		x_c2_att_w = None
		return PICASACommonOut(h_c1,h_c2,z_c1,z_c2,x_c1_att_w,x_c2_att_w)


###### PICASA UNIQUE MODEL #######

class PICASAUniqueNet(nn.Module):
	def __init__(self,input_dim,common_latent_dim,unique_latent_dim,enc_layers,dec_layers,num_batches):
		super(PICASAUniqueNet,self).__init__()
		self.u_encoder = MLP(input_dim,enc_layers)

		concat_dim = common_latent_dim + unique_latent_dim 
		self.u_decoder = MLP(concat_dim,dec_layers)
  
		decoder_in_dim = dec_layers[len(dec_layers)-1] 
   
		self.zinb_scale = nn.Linear(decoder_in_dim, input_dim) 
		self.zinb_dropout = nn.Linear(decoder_in_dim, input_dim)
		self.zinb_dispersion = nn.Parameter(torch.randn(input_dim), requires_grad=True)
		
		self.batch_discriminator = nn.Linear(unique_latent_dim, num_batches)

	
	def forward(self,x_c1,x_zcommon):	
   
		z_unique = self.u_encoder(x_c1.float())
		
		h = self.u_decoder(torch.cat((x_zcommon, z_unique), dim=1))
  
		px_scale = torch.exp(self.zinb_scale(h))  
		px_dropout = self.zinb_dropout(h)  
		px_rate = self.zinb_dispersion.exp()
  
		batch_pred = self.batch_discriminator(z_unique)
		
		return z_unique,px_scale,px_rate,px_dropout,batch_pred


	def get_common_unique_representation(self,x_gene):
		h = torch.log(torch.tensor(x_gene) + 1e-8).T  
		# h = h - self.zinb_scale.bias  
		h = torch.matmul(h, self.zinb_scale.weight)

		current_input = h
		for layer in reversed(self.u_decoder.fc.layers): 
			if isinstance(layer, nn.Linear):
				# current_input = current_input - layer.bias  
				current_input = torch.matmul(current_input, layer.weight)
			# elif isinstance(layer, nn.BatchNorm1d):
			# 	current_input = current_input * layer.running_var.sqrt() + layer.running_mean
			# elif isinstance(layer, nn.ReLU):
			# 	current_input = torch.clamp(current_input, min=0)  
			elif isinstance(layer, nn.Dropout):
				pass
			else:
				pass

		z_common_dim = self.u_decoder.fc.layers[0].in_features - self.u_encoder.fc.layers[-4].out_features
		z_common = current_input[:, :z_common_dim]
		z_unique = current_input[:, z_common_dim:]

		return h,z_common, z_unique

###### PICASA BASE MODEL #######

class PICASABaseNet(nn.Module):
	def __init__(self,input_dim,latent_dim,enc_layers,dec_layers,num_batches):
		super(PICASABaseNet,self).__init__()
  
		self.u_encoder = MLP(input_dim,enc_layers)
		self.u_decoder = MLP(latent_dim,dec_layers)
  
		decoder_in_dim = dec_layers[len(dec_layers)-1]  
		self.zinb_scale = nn.Linear(decoder_in_dim, input_dim) 
		self.zinb_dropout = nn.Linear(decoder_in_dim, input_dim)
		self.zinb_dispersion = nn.Parameter(torch.randn(input_dim), requires_grad=True)
		
		self.batch_discriminator = nn.Linear(latent_dim, num_batches)

	
	def forward(self,x_c1):	
 
		row_sums = x_c1.sum(dim=1, keepdim=True)
		x_norm = torch.div(x_c1, row_sums) * 1e4
  
		z = self.u_encoder(x_norm.float())
		h = self.u_decoder(z)
  
		px_scale = torch.exp(self.zinb_scale(h))  
		px_dropout = self.zinb_dropout(h)  
		px_rate = self.zinb_dispersion.exp()
  
		batch_pred = self.batch_discriminator(z)
		
		return z,px_scale,px_rate,px_dropout,batch_pred

